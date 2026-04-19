from cube_explorer.core import execute_sequence
from cube_explorer.visualization import plot_cube_walk
from cube_explorer.grammars.sefer import GRAMMAR

path, symbols, score = execute_sequence(
    start=0,
    symbols=["א", "מ", "ש", "א"],
    grammar=GRAMMAR,
)

print("Path:", path)
print("Score:", score)

fig = plot_cube_walk(path)
fig.show()
