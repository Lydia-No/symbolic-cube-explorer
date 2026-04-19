# Status and Boundaries

This document clarifies the role of `symbolic-cube-explorer` within the current local ecosystem.

## Canonical repository

The canonical public and conceptual entry point is:

- `/home/linlin/symbolic-cube-explorer`

This is the repository that should be treated as the main reference point for the symbolic systems stack.

## Workspace repository

The following repository acts primarily as a development workspace and orchestration shell:

- `/home/linlin/cube-lab`

`cube-lab` contains bootstrap scripts, integration tests, and nested or linked development copies of related repositories. It is important for local development, but it is not the primary public entry point.

## Parallel or nested copies

There are nested copies or linked working versions of repositories inside `cube-lab/`.

These should be treated as workspace-local development artifacts unless explicitly promoted.

In particular:

- `cube-lab/symbolic-cube-explorer`
- `cube-lab/symbolic-dynamics-lab`
- `cube-lab/symbolic-engine/symbolic-dynamics-engine`

These may be useful for development and integration, but the top-level repository remains canonical.

## Package layout note

The current `symbolic-cube-explorer` repository contains both:

- `src/cube_explorer/`
- `symbolic_cube_explorer/`

This suggests a partial transition or coexistence between source layouts.

Until cleanup is complete:

- treat `src/cube_explorer/` as the primary package path
- treat parallel package artifacts as legacy, transitional, or experimental unless confirmed otherwise

## Working rule

When in doubt:

1. use `/home/linlin/symbolic-cube-explorer` as the source of truth
2. treat `cube-lab` as workspace/integration infrastructure
3. avoid assuming nested copies are authoritative
