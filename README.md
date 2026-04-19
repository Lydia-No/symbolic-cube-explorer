# Symbolic Cube Explorer

Symbolic Cube Explorer is the canonical entry point to the symbolic systems ecosystem.

It is the clearest starting place for understanding the broader stack of symbolic state-space exploration, symbolic dynamics, observer-based traversal, experimental labs, and governance-oriented applications.

At its core, this project models systems as structured spaces of possible states, then studies how symbols, operators, and constraints generate trajectories through those spaces.

## Why start here

This repository is the best entry point because it already contains the strongest balance of:

- core symbolic structure
- concrete geometry
- experiments
- examples
- analysis tools
- visualization hooks

It is close enough to the mathematical center to be foundational, while still concrete enough to explore directly.

## Local ecosystem map

### One-line repo identities

- `symbolic-cube-explorer` — symbolic state-space exploration engine for cube and hypercube-like discrete geometries
- `cube-lab` — development workspace and orchestration shell for linked symbolic repositories and integration tests
- `symbolic-system-core` — R-based framework for symbolic transformation systems, discrete dynamics, and experiments
- `symbolic-apps` — R/Shiny application layer for interactive symbolic system models
- `Lydia-No` — public GitHub profile repository and ecosystem landing point

## Dependency chain

The current ecosystem is easiest to understand in this order:

`symbolic-system-core`  
→ symbolic transformation logic, experiments, solvers, and evaluation in R

`symbolic-cube-explorer`  
→ symbolic state-space geometry, transitions, trajectories, and exploration in Python

`cube-lab`  
→ workspace shell for orchestrating linked repositories, integration tests, and development flows

`symbolic-apps`  
→ application-facing R/Shiny layer for interacting with symbolic system logic

`Lydia-No`  
→ public-facing profile and ecosystem landing point

### How to read that chain

- `symbolic-system-core` carries part of the symbolic systems logic and experimentation branch in R
- `symbolic-cube-explorer` is the clearest concrete expression of the symbolic state-space idea in Python
- `cube-lab` is not the canonical public entry point; it is the development workspace and integration shell
- `symbolic-apps` sits closer to interface and application use
- `Lydia-No` is the public identity layer

### Practical reading order

For a new technical visitor:

1. `symbolic-cube-explorer`
2. `cube-lab`
3. `symbolic-system-core`
4. `symbolic-apps`
5. `Lydia-No`

### Practical development order

For local work:

1. understand `symbolic-cube-explorer`
2. inspect how `cube-lab` orchestrates workspace components
3. inspect `symbolic-system-core` for the R-side symbolic logic
4. inspect `symbolic-apps` for app-facing integration

## Internal structure of this repository

The repository currently contains several important layers.

### Package source
- `src/cube_explorer/` — main implementation package
- `src/cube_explorer/analysis.py`
- `src/cube_explorer/attractors.py`
- `src/cube_explorer/core.py`
- `src/cube_explorer/experiments.py`
- `src/cube_explorer/grammar.py`
- `src/cube_explorer/graycode.py`
- `src/cube_explorer/hypercube.py`
- `src/cube_explorer/symmetry.py`
- `src/cube_explorer/transitions.py`
- `src/cube_explorer/visualization.py`

### Exploratory modules
- `src/cube_explorer/analysis/`
- `src/cube_explorer/entropy/`
- `src/cube_explorer/grammars/`
- `src/cube_explorer/walkers/`

### Examples
- `examples/` — runnable examples for walks, entropy, grammar analysis, transition graphs, and visualization

### Experiments
- `experiments/` — universe scans, rule extraction, exploration demos, transition demos, and evolution experiments

### Tests
- `tests/` — basic validation for determinism and grammar behavior

## Research vs application split

### Research and engine repositories

These repositories are primarily for symbolic modeling, state-space exploration, experiments, and development infrastructure.

- `symbolic-cube-explorer`
- `cube-lab`
- `symbolic-system-core`

### Application and interface repositories

These repositories are closer to user-facing interaction, public entry, or app-layer use.

- `symbolic-apps`
- `Lydia-No`

This distinction matters because the ecosystem has two different modes:

- research mode, where symbolic dynamics and structured state-space ideas are developed
- application mode, where those ideas are surfaced through interfaces, demos, or public presence

## Conceptual stack

A simple view of the stack looks like this:

`symbolic-system-core`  
→ symbolic system logic and experiments in R

`symbolic-cube-explorer`  
→ symbolic state-space geometry and transition exploration in Python

`cube-lab`  
→ workspace orchestration, linked experimentation, and integration shell

`symbolic-apps`  
→ application-facing R/Shiny layer

In a broader conceptual sense:

symbols  
→ operators

operators  
→ transitions

transitions  
→ trajectories

trajectories  
→ structure, attractors, and discoverable system behavior

## What this project can be used for

- symbolic state-space exploration
- hypercube and discrete geometry traversal
- attractor discovery
- entropy and transition analysis
- grammar-driven symbolic walks
- observer and walker experiments
- foundations for symbolic AI or neural-symbolic architectures
- governance and compliance modeling through structured state transitions

## Quick start

Create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
