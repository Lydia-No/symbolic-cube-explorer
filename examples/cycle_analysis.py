from cube_explorer.core import execute_sequence
from cube_explorer.grammars.sefer import GRAMMAR


def find_cycle(path):
    visited = {}

    for i, state in enumerate(path):
        if state in visited:
            start = visited[state]
            cycle = path[start:i]
            return cycle
        visited[state] = i

    return None


start_state = 0
sequence = ["א", "מ", "ש", "א", "מ", "ש", "א"]

path, symbols, score = execute_sequence(
    start=start_state,
    symbols=sequence,
    grammar=GRAMMAR,
)

print("Grammar:", GRAMMAR.metadata().display_name)
print("Sequence:", symbols)
print("Path:", path)
print("Score:", score)

cycle = find_cycle(path)

if cycle:
    print("Cycle detected:", cycle)
else:
    print("No cycle detected")
