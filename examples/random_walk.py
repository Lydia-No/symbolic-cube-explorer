import random

from cube_explorer.core import run_symbol_sequence
from cube_explorer.grammars.sefer import apply_sefer_symbol

symbols = ["א","מ","ש"]

sequence = [random.choice(symbols) for _ in range(50)]

path = run_symbol_sequence(0, sequence, apply_sefer_symbol)

print("Sequence:", sequence)
print("Path:", path)
print("Unique states visited:", len(set(path)))
