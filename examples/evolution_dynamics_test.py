import random
from collections import Counter

# ======================
# GLOBAL PARAMETERS
# ======================

AXES = [1, 2, 4, 8]

MAX_LEN = 80
WINDOW = 20

POP_SIZE = 30
GENERATIONS = 20
MUTATION_RATE = 0.3


# ======================
# FIELD FUNCTIONS
# ======================

def local_diversity(seq, window=WINDOW):
    if len(seq) == 0:
        return 0

    if len(seq) <= window:
        return len(set(seq)) / len(seq)

    samples = []
    for i in range(0, len(seq) - window + 1, window):
        chunk = seq[i:i+window]
        samples.append(len(set(chunk)) / len(chunk))

    return sum(samples) / len(samples)


def symmetry_score(seq):
    return sum(1 for i in range(len(seq)//2) if seq[i] == seq[-i-1])


# ======================
# REPAIR (MINIMAL CLOSURE)
# ======================

def repair(seq):
    counts = Counter(seq)
    repaired = list(seq)

    MAX_REPAIR = 4
    added = 0

    for axis, c in counts.items():
        if c % 2 != 0 and added < MAX_REPAIR:
            repaired.append(axis)
            added += 1

    return repaired


# ======================
# MUTATION
# ======================

def mutate(seq):
    new_seq = list(seq)

    # insertion
    if random.random() < 0.5 and len(new_seq) < MAX_LEN:
        new_seq.append(random.choice(AXES))

    # modification
    if len(new_seq) > 0 and random.random() < 0.5:
        i = random.randrange(len(new_seq))
        new_seq[i] = random.choice(AXES)

    # deletion
    if len(new_seq) > 2 and random.random() < 0.3:
        i = random.randrange(len(new_seq))
        del new_seq[i]

    return new_seq


# ======================
# FITNESS (THE CORE FIELD)
# ======================

def score(seq):
    if len(seq) == 0:
        return -10

    if len(seq) > MAX_LEN:
        return -10

    s = 0

    # local identity field
    if local_diversity(seq) < 0.5:
        s -= 5

    # symmetry (soft attractor)
    s += symmetry_score(seq) * 0.5

    # length penalty
    s -= len(seq) * 0.2

    # compression efficiency
    unique = len(set(seq))
    if unique > 0:
        compression = len(seq) / unique
        s -= compression * 0.5

    return s


# ======================
# INITIAL POPULATION
# ======================

def random_seq():
    return [random.choice(AXES) for _ in range(random.randint(4, 12))]


# ======================
# EVOLUTION LOOP
# ======================

def run():
    population = [random_seq() for _ in range(POP_SIZE)]

    for gen in range(GENERATIONS):

        scored = []

        for seq in population:
            mutated = mutate(seq)
            repaired = repair(mutated)
            fitness = score(repaired)

            scored.append((fitness, repaired))

        # sort by fitness
        scored.sort(key=lambda x: x[0], reverse=True)

        best_score, best_seq = scored[0]

        print(f"Gen {gen}: best score = {best_score:.2f}, len = {len(best_seq)}")
        print(f"  seq = {best_seq}\n")

        # selection: top half survives
        survivors = [seq for _, seq in scored[:POP_SIZE // 2]]

        # reproduce
        new_population = survivors.copy()
        while len(new_population) < POP_SIZE:
            parent = random.choice(survivors)
            child = mutate(parent)
            new_population.append(child)

        population = new_population


# ======================
# ENTRY
# ======================

if __name__ == "__main__":
    run()
