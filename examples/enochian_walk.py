from cube_explorer.core import execute_sequence
from cube_explorer.grammars.enochian import GRAMMAR

start_state = 0
sequence = ["OL", "PA", "NA", "OL"]

path, symbols, score = execute_sequence(
    start=start_state,
    symbols=sequence,
    grammar=GRAMMAR,
)

print("Grammar:", GRAMMAR.metadata().display_name)
print("Sequence:", symbols)
print("Path:", path)
print("Score:", score)
