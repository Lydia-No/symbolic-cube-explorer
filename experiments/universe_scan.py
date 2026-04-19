import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from symbolic_cube_explorer.core import CubeGraph
from symbolic_cube_explorer.exploration.engine import ExplorationEngine
from symbolic_cube_explorer.analysis.attractors import find_attractors
from symbolic_cube_explorer.metrics.entropy import shannon_entropy


def random_forbidden(dim, k=2):
    states = []
    for i in range(2 ** dim):
        b = format(i, f"0{dim}b")
        states.append(b)

    return set(random.sample(states, k))


def run_experiment(dim=4, forbidden=None, steps=500):
    cube = CubeGraph(dim=dim, forbidden=forbidden)
    start = cube.random_vertex()

    engine = ExplorationEngine(cube)
    trajectory = engine.walk(start, steps=steps)

    entropy = shannon_entropy(trajectory)
    attractors = find_attractors(trajectory, window=5, min_repeats=3)

    total_strength = sum(count for _, count in attractors)

    return {
        "forbidden": forbidden,
        "entropy": entropy,
        "num_attractors": len(attractors),
        "strength": total_strength,
    }


def main():
    results = []

    for _ in range(30):  # number of universes
        forbidden = random_forbidden(dim=4, k=2)

        res = run_experiment(dim=4, forbidden=forbidden)
        results.append(res)

    # sort by attractor strength
    results.sort(key=lambda x: x["strength"], reverse=True)

    print("\n=== TOP STRUCTURED UNIVERSES ===\n")

    for r in results[:5]:
        print("Forbidden:", r["forbidden"])
        print("Entropy:", round(r["entropy"], 4))
        print("Attractors:", r["num_attractors"])
        print("Strength:", r["strength"])
        print("-" * 40)


if __name__ == "__main__":
    main()
