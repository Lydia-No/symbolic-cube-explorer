from cube_explorer.core import execute_sequence
from cube_explorer.hypercube import Hypercube
from cube_explorer.grammars.sefer import GRAMMAR

cube = Hypercube(3)

sequence = ["א", "מ", "ש"] * 10

path, symbols, score = execute_sequence(
    start=0,
    symbols=sequence,
    grammar=GRAMMAR,
)

print("Cube dim:", cube.dim)
print("Grammar:", GRAMMAR.metadata().display_name)
print("Sequence length:", len(symbols))
print("Path length:", len(path))
print("Unique states visited:", len(set(path)))
print("Score:", score)
print("Path:", path)
