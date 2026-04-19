import sys
import os
import random

sys.path.append(os.path.abspath("src"))

from cube_explorer.core import CubeGraph
from cube_explorer.utils import score_sequence

cube = CubeGraph()


# --- basic tools ---

def random_walk(start=0, length=6):
    path = [start]
    current = start

    for _ in range(length):
        neighbors = cube.neighbors(current)
        current = random.choice(neighbors)
        path.append(current)

    return path


def path_to_deltas(path):
    return [path[i+1] ^ path[i] for i in range(len(path)-1)]


def mutate(deltas):
    """randomly tweak one position"""
    new = deltas[:]
    idx = random.randint(0, len(new)-1)
    new[idx] = random.choice([1, 2, 4])
    return new


def deltas_to_path(start, deltas):
    path = [start]
    current = start

    for d in deltas:
        current = current ^ d
        path.append(current)

    return path


# --- evolution ---

def evolve():
    print("\nEVOLUTION RUN\n")

    population_size = 100
    generations = 20

    # initial population
    population = []
    for _ in range(population_size):
        path = random_walk(0, length=6)
        deltas = path_to_deltas(path)
        population.append(deltas)

    for g in range(generations):
        scored = []

        for d in population:
            score = score_sequence(d)
            scored.append((score, d))

        # sort by score
        scored.sort(reverse=True, key=lambda x: x[0])

        # print best
        best_score, best_seq = scored[0]
        print(f"Gen {g}: best score = {best_score}, seq = {best_seq}")

        # select top 20
        top = [d for _, d in scored[:20]]

        # reproduce + mutate
        new_population = []

        while len(new_population) < population_size:
            parent = random.choice(top)
            child = mutate(parent)
            new_population.append(child)

        population = new_population


if __name__ == "__main__":
    evolve()
