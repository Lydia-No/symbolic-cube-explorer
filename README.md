# Symbolic Cube Explorer
## Symbols as operators on discrete geometric state spaces

Symbolic Cube Explorer is a small research framework for treating **symbol sequences as executable dynamics** rather than static tokens.

**Core idea:** a symbol is defined by what it *does* to a system state.  
A sequence of symbols becomes an **operator program** that produces a **trajectory** through a finite state space.  
Structure is then measured directly from the trajectory: recurrence, closure, symmetry, motifs, and stability.

This is not a language model. It is a **laboratory** for operational semantics: explicit state spaces, explicit transitions, and measurable outcomes.

---

## What this project studies

Most symbolic and NLP systems treat symbols as objects to interpret. This project instead treats symbols as **state transformations**:

- **Symbol** → operator
- **Sequence** → program
- **Execution** → path through a graph
- **Meaning/structure** → measurable properties of that path

The goal is to make symbolic behavior **inspectable** and **testable** in a small world where every state and transition is explicit.

---

## The state space (default: Q₃ cube)

The default substrate is the 3D hypercube graph **Q₃**:

- 8 vertices (3-bit states)
- 12 edges
- each step flips exactly **one bit** (minimal discrete change)

Because Q₃ is fully enumerable and easy to visualize, it’s a good “first lab” for symbolic dynamics.

---

## How it works (pipeline)

A typical run looks like this:

1. **Initialize** a start state (e.g. seeded from a concept string).
2. **Execute** an operator sequence (or generate one from rules).
3. **Record** the resulting trajectory: states + emitted symbols.
4. **Score/measure** structural features of the trajectory.

This produces a compact artifact you can compare across inputs:
- start vertex
- state path
- symbol sequence
- feature vector / score

---

## Installation

Create venv + install editable:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
from cube_explorer.core import CubeGraph, SymbolicWalker

cube = CubeGraph()
walker = SymbolicWalker(cube)

start, path, seq, score = walker.run_concept("collective intelligence")

print("Start:", start)
print("Path:", path)
print("Sequence:", " → ".join(seq))
print("Score:", score)
python -m cube_explorer "collective intelligence"
python -m cube_explorer "collective intelligence" --plot
python -m cube_explorer "collective intelligence" --html walk.html
python -m cube_explorer "collective intelligence" --json
exit()
exit ()
exit()
