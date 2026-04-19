# symbolic-cube-explorer Migration Log

This file records migrated material brought into symbolic-cube-explorer from earlier repositories.

## Format

- Source repo:
- Source path:
- Source commit SHA:
- Destination path:
- Action:
- Notes:

---

## Initial migrations

### Engine base
- Source repo: Lydia-No/symbolic-cube-explorer
- Source path: src/
- Source commit SHA: c14f43eafc653cdc8567adee7d8c3d5d30df64c6
- Destination path: src/
- Action: kept as canonical base
- Notes: canonical engine implementation

### Donor imports from cube-core
- Source repo: Lydia-No/The-cube
- Source path: packages/cube-core/src/cube_explorer/utils.py
- Source commit SHA: 95ae6bc52bf5bffaafe583d40e72dc7beed8f339
- Destination path: src/cube_explorer/utils.py
- Action: copied
- Notes: includes approved empty-sequence handling improvement

- Source repo: Lydia-No/The-cube
- Source path: packages/cube-core/src/cube_explorer/visualization.py
- Source commit SHA: ad8f4459e980a843f0c3fad0b68e048f335024b3
- Destination path: src/cube_explorer/visualization.py
- Action: copied
- Notes: approved donor visualization improvement

- Source repo: Lydia-No/The-cube
- Source path: packages/cube-core/docs/philosophy.md
- Source commit SHA: 95ae6bc52bf5bffaafe583d40e72dc7beed8f339
- Destination path: docs/imported/cube-core/philosophy.md
- Action: copied
- Notes: donor conceptual documentation

### Manual resolutions
- Source repo: Lydia-No/The-cube and Lydia-No/symbolic-cube-explorer
- Source path: packages/cube-core/src/cube_explorer/__init__.py and src/cube_explorer/__init__.py
- Source commit SHA: ad8f4459e980a843f0c3fad0b68e048f335024b3 and c14f43eafc653cdc8567adee7d8c3d5d30df64c6
- Destination path: src/cube_explorer/__init__.py
- Action: merged manually
- Notes: resolved into deliberate current engine export surface

- Source repo: Lydia-No/symbolic-cube-explorer and Lydia-No/The-cube
- Source path: src/cube_explorer/attractors.py and packages/cube-core/src/cube_explorer/attractors.py
- Source commit SHA: c14f43eafc653cdc8567adee7d8c3d5d30df64c6 and ad8f4459e980a843f0c3fad0b68e048f335024b3
- Destination path: src/cube_explorer/attractors.py
- Action: merged manually
- Notes: kept canonical engine implementation and made the public surface explicit; donor semantics were not imported blindly

- Source repo: Lydia-No/The-cube
- Source path: packages/cube-core/src/cube_explorer/hamiltonian.py
- Source commit SHA: ad8f4459e980a843f0c3fad0b68e048f335024b3
- Destination path: src/cube_explorer/hamiltonian.py
- Action: adapted manually
- Notes: imported as a donor utility and rewritten against the current CubeGraph neighbors()/dims API
