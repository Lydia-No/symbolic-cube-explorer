import sys
import os
import random
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from symbolic_cube_explorer.core import CubeGraph
from symbolic_cube_explorer.exploration.engine import ExplorationEngine
from symbolic_cube_explorer.analysis.attractors import find_attractors, attractor_signature
from symbolic_cube_explorer.metrics.entropy import shannon_entropy


DIM = 4
FORBIDDEN_SIZE = 2
POP_SIZE = 20
GENERATIONS = 10

STATE_POOL = [format(i, f"0{DIM}b") for i in range(2 ** DIM)]


def random_universe():
    transitions = []
    for _ in range(FORBIDDEN_SIZE):
        a = random.choice(STATE_POOL)
        b = random.choice(STATE_POOL)
        transitions.append((a, b))
    return set(transitions)


def mutate(universe):
    universe = set(universe)

    if random.random() < 0.5:
        universe.pop()
        a = random.choice(STATE_POOL)
        b = random.choice(STATE_POOL)
        universe.add((a, b))

    return universe


def fitness(universe):
    cube = CubeGraph(dim=DIM, forbidden_transitions=universe)

    start = cube.random_vertex()
    engine = ExplorationEngine(cube)

    trajectory = engine.walk(start, steps=300)

    entropy = shannon_entropy(trajectory)
    attractors = find_attractors(trajectory, window=5, min_repeats=3)
    signature = attractor_signature(attractors)

    # --- target: strong simple cycles ---
    target = 4

    signature_score = signature.get(target, 0)

    # reward multiple attractors
    structure_score = len(attractors)

    entropy_penalty = abs(2.6 - entropy)

    score = signature_score * 2 + structure_score * 2 - entropy_penalty * 10

    return score, entropy, len(attractors), signature


    return score, entropy, len(attractors), signature


def evolve():
    population = [random_universe() for _ in range(POP_SIZE)]

    for gen in range(GENERATIONS):
        scored = []

        for u in population:
            score, entropy, n_attr, signature = fitness(u)
            scored.append((score, u, entropy, n_attr, signature))

        scored.sort(reverse=True, key=lambda x: x[0])

        print(f"\n=== GENERATION {gen} ===")

        for s in scored[:3]:
            print("Transitions:", s[1])
            print("Score:", round(s[0], 3),
                  "| Entropy:", round(s[2], 3),
                  "| Attractors:", s[3],
                  "| Signature:", s[4])
            print("-" * 40)

        survivors = [u for _, u, _, _, _ in scored[:POP_SIZE // 2]]

        new_population = []
        while len(new_population) < POP_SIZE:
            parent = random.choice(survivors)
            child = mutate(parent)
            new_population.append(child)

        population = new_population


if __name__ == "__main__":
    evolve()
