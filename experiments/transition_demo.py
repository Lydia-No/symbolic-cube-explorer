import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from symbolic_cube_explorer.core import CubeGraph
from symbolic_cube_explorer.exploration.engine import ExplorationEngine
from symbolic_cube_explorer.analysis.attractors import find_attractors, attractor_signature
from symbolic_cube_explorer.metrics.entropy import shannon_entropy


def main():
    forbidden_transitions = {
        ("0001", "0011"),
    }

    cube = CubeGraph(dim=4, forbidden_transitions=forbidden_transitions)

    start = cube.random_vertex()
    engine = ExplorationEngine(cube)

    trajectory = engine.walk(start, steps=500)

    entropy = shannon_entropy(trajectory)
    attractors = find_attractors(trajectory, window=5, min_repeats=3)
    signature = attractor_signature(attractors)

    print("Entropy:", entropy)
    print("Attractors:", len(attractors))
    print("Signature:", signature)


if __name__ == "__main__":
    main()
