import random
from collections import Counter


AXES = [1, 2, 4, 8]


def random_sequence(length=8):
    return [random.choice(AXES) for _ in range(length)]


def distance_to_closure(seq):
    counts = Counter(seq)
    return sum(1 for v in counts.values() if v % 2 != 0)


def get_unpaired_axes(seq):
    counts = Counter(seq)
    return [axis for axis, c in counts.items() if c % 2 != 0]


def repair_step(seq):
    """
    One step toward closure:
    pick an unpaired axis and add it
    """
    unpaired = get_unpaired_axes(seq)

    if not unpaired:
        return seq  # already closed

    axis = random.choice(unpaired)
    return seq + [axis]


def relax(seq, max_steps=10):
    history = [seq]

    current = seq

    for _ in range(max_steps):
        if distance_to_closure(current) == 0:
            break

        current = repair_step(current)
        history.append(current)

    return history


def run(samples=5):
    print("\nRELAXATION DYNAMICS\n")

    for _ in range(samples):
        seq = random_sequence()

        print("START:", seq, "| distance =", distance_to_closure(seq))

        history = relax(seq)

        for step, s in enumerate(history[1:], start=1):
            print(f" step {step}: {s} | distance = {distance_to_closure(s)}")

        print("-" * 40)


if __name__ == "__main__":
    run()
