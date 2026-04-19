# Architecture Notes

## Current reality

The local system has two overlapping structures:

### 1. Standalone repositories in `/home/linlin`
These are the clean top-level repositories.

### 2. Nested development workspace inside `cube-lab/`
This contains linked or copied working versions of related repositories.

This means:

- `symbolic-cube-explorer` should remain the canonical public and conceptual entry point
- `cube-lab` should be treated as a development workspace and orchestration shell
- `symbolic-system-core` and `symbolic-apps` form an R-based application and experimentation branch

## Recommended high-level interpretation

- `symbolic-cube-explorer` = center of symbolic geometry and exploration
- `cube-lab` = workspace/integration shell
- `symbolic-system-core` = symbolic system engine in R
- `symbolic-apps` = application layer
- `Lydia-No` = public identity layer

## Long-term cleanup direction

Over time, the ecosystem should become easier to read by clarifying:

- what is canonical
- what is legacy
- what is workspace-only
- what is experimental
- what is application-facing

This document exists to keep that distinction visible.
