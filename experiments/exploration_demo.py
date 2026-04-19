import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from symbolic_cube_explorer.core import CubeGraph
from symbolic_cube_explorer.exploration.engine import ExplorationEngine
from symbolic_cube_explorer.analysis.attractors import find_attractors
from symbolic_cube_explorer.metrics.entropy import shannon_entropy


def main():
    # --- define forbidden states ---
    forbidden = {"0000", "1111"}  # extreme states removed

    cube = CubeGraph(dim=4, forbidden=forbidden)
    start = cube.random_vertex()

    engine = ExplorationEngine(cube)
    trajectory = engine.walk(start, steps=500)

    entropy = shannon_entropy(trajectory)
    attractors = find_attractors(trajectory, window=5, min_repeats=3)

    print("Forbidden states:", forbidden)
    print("Start:", start)
    print("Entropy:", entropy)
    print("Strong attractors:", len(attractors))

    for a, count in attractors[:5]:
        print("Attractor:", a, "| repeats:", count)


if __name__ == "__main__":
    main()
