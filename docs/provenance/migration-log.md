# symbolic-cube-explorer Migration Log

This file records migrated material brought into symbolic-cube-explorer from earlier repositories.

## Repository migration metadata

- Migration date: 2026-04-19
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Notes: destination commit above is the final-repo baseline that received the migrated material before this provenance log was expanded to include timeline metadata.

## Format

- Source working tree:
- Source remote:
- Source path:
- Source commit SHA:
- Source commit date:
- Destination repo:
- Destination path:
- Destination commit SHA:
- Destination commit date:
- Migration date:
- Action:
- Notes:

---

## Initial migrations

### Engine base
- Source working tree: ~/symbolic-cube-explorer
- Source remote: Lydia-No/symbolic-cube-explorer
- Source path: src/
- Source commit SHA: c14f43eafc653cdc8567adee7d8c3d5d30df64c6
- Source commit date: 2026-03-23T22:15:36+01:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: src/
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: kept as canonical base
- Notes: canonical engine implementation

### Donor imports from cube-core
- Source working tree: ~/the-cube
- Source remote: Lydia-No/The-cube
- Source path: packages/cube-core/src/cube_explorer/utils.py
- Source commit SHA: 95ae6bc52bf5bffaafe583d40e72dc7beed8f339
- Source commit date: 2026-04-17T19:31:59+02:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: src/cube_explorer/utils.py
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: copied
- Notes: includes approved empty-sequence handling improvement

- Source working tree: ~/the-cube
- Source remote: Lydia-No/The-cube
- Source path: packages/cube-core/src/cube_explorer/visualization.py
- Source commit SHA: ad8f4459e980a843f0c3fad0b68e048f335024b3
- Source commit date: 2026-04-17T19:47:09+02:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: src/cube_explorer/visualization.py
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: copied
- Notes: approved donor visualization improvement

- Source working tree: ~/the-cube
- Source remote: Lydia-No/The-cube
- Source path: packages/cube-core/docs/philosophy.md
- Source commit SHA: 95ae6bc52bf5bffaafe583d40e72dc7beed8f339
- Source commit date: 2026-04-17T19:31:59+02:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: docs/imported/cube-core/philosophy.md
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: copied
- Notes: donor conceptual documentation

### Manual resolutions
- Source working tree: ~/the-cube and ~/symbolic-cube-explorer
- Source remote: Lydia-No/The-cube and Lydia-No/symbolic-cube-explorer
- Source path: packages/cube-core/src/cube_explorer/__init__.py and src/cube_explorer/__init__.py
- Source commit SHA: ad8f4459e980a843f0c3fad0b68e048f335024b3 and c14f43eafc653cdc8567adee7d8c3d5d30df64c6
- Source commit date: 2026-04-17T19:47:09+02:00 and 2026-03-23T22:15:36+01:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: src/cube_explorer/__init__.py
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: merged manually
- Notes: resolved into deliberate current engine export surface

- Source working tree: ~/symbolic-cube-explorer and ~/the-cube
- Source remote: Lydia-No/symbolic-cube-explorer and Lydia-No/The-cube
- Source path: src/cube_explorer/attractors.py and packages/cube-core/src/cube_explorer/attractors.py
- Source commit SHA: c14f43eafc653cdc8567adee7d8c3d5d30df64c6 and ad8f4459e980a843f0c3fad0b68e048f335024b3
- Source commit date: 2026-03-23T22:15:36+01:00 and 2026-04-17T19:47:09+02:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: src/cube_explorer/attractors.py
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: merged manually
- Notes: kept canonical engine implementation and made the public surface explicit; donor semantics were not imported blindly

- Source working tree: ~/the-cube
- Source remote: Lydia-No/The-cube
- Source path: packages/cube-core/src/cube_explorer/hamiltonian.py
- Source commit SHA: ad8f4459e980a843f0c3fad0b68e048f335024b3
- Source commit date: 2026-04-17T19:47:09+02:00
- Destination repo: Lydia-No/symbolic-cube-explorer
- Destination path: src/cube_explorer/hamiltonian.py
- Destination commit SHA: bf7b06a41ffc1756a581ae078a3739e444b80b6a
- Destination commit date: 2026-04-19T03:30:30+02:00
- Migration date: 2026-04-19
- Action: adapted manually
- Notes: imported as a donor utility and rewritten against the current CubeGraph neighbors()/dims API
