from cube_explorer.core import execute_sequence
from cube_explorer.grammars.runes import GRAMMAR

start_state = 0
sequence = ["ᚠ", "ᚢ", "ᚦ", "ᚠ"]

path, symbols, score = execute_sequence(
    start=start_state,
    symbols=sequence,
    grammar=GRAMMAR,
)

print("Grammar:", GRAMMAR.metadata().display_name)
print("Sequence:", symbols)
print("Path:", path)
print("Score:", score)
