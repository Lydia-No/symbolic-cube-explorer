# Dependency Chain

This document explains the practical dependency and reading order across the current local symbolic systems ecosystem.

## High-level chain

The current ecosystem is best understood in this order:

`symbolic-system-core`
→ symbolic transformation logic, experiments, solvers, and evaluation in R

`symbolic-cube-explorer`
→ symbolic state-space geometry, transitions, trajectories, and exploration in Python

`cube-lab`
→ workspace shell for orchestrating linked repositories, integration tests, and development flows

`symbolic-apps`
→ application-facing R/Shiny layer for interacting with symbolic system logic

## Repository roles in dependency terms

### `symbolic-system-core`
This is a symbolic systems and experiment engine in R.

It appears to contain:
- core system logic
- experiment runners
- solvers
- generators
- supply-chain / ArcTopia-related modeling
- evaluation and export scripts

It is conceptually upstream for symbolic modeling logic in the R branch.

### `symbolic-cube-explorer`
This is the canonical exploration engine in Python.

It appears to contain:
- cube and hypercube representations
- symbolic transitions
- grammar-based movement
- attractor and entropy analysis
- experiments and examples
- visualization support

It is the canonical public entry point because it is the clearest concrete expression of the symbolic state-space idea.

### `cube-lab`
This is not the canonical public entry point.
It is a development workspace and orchestration shell.

It appears to contain:
- bootstrap scripts
- setup scripts
- integration tests
- tools
- nested or linked copies of related repositories

It is downstream as a workspace shell, but upstream in practical development flow because it coordinates local work.

### `symbolic-apps`
This is the application-facing layer in the R branch.

It appears to contain:
- Shiny app code
- solver access
- symbolic application logic

It is downstream from symbolic modeling logic and closer to end-user interaction.

## Practical reading order

For a new technical visitor:

1. `symbolic-cube-explorer`
2. `cube-lab`
3. `symbolic-system-core`
4. `symbolic-apps`

## Practical development order

For local development:

1. understand `symbolic-cube-explorer`
2. inspect how `cube-lab` orchestrates workspace components
3. inspect `symbolic-system-core` for R-side symbolic logic
4. inspect `symbolic-apps` for app-facing integration

## Working rule

When explaining the ecosystem publicly:

- start with `symbolic-cube-explorer`
- mention `cube-lab` as the development workspace
- mention `symbolic-system-core` as the R symbolic systems branch
- mention `symbolic-apps` as the app layer

## Future cleanup target

Over time, this chain should become even clearer by distinguishing:

- canonical public repositories
- workspace-only repositories
- core engines
- application layers
- legacy or parallel package layouts
