import random

from cube_explorer.core import execute_sequence
from cube_explorer.analysis import entropy
from cube_explorer.grammars.sefer import GRAMMAR


def find_cycle(path):
    visited = {}

    for i, state in enumerate(path):
        if state in visited:
            start = visited[state]
            return path[start:i]
        visited[state] = i

    return None


symbols = ["א", "מ", "ש"]
sequence = [random.choice(symbols) for _ in range(100)]

path, used_symbols, score = execute_sequence(
    start=0,
    symbols=sequence,
    grammar=GRAMMAR,
)

print("Grammar:", GRAMMAR.metadata().display_name)
print("Sequence length:", len(used_symbols))
print("Path length:", len(path))
print("Unique states visited:", len(set(path)))
print("State entropy:", entropy(path))
print("Symbol entropy:", entropy(used_symbols))
print("Score:", score)

cycle = find_cycle(path)
print("Cycle detected:", cycle)

print("Path:", path)
