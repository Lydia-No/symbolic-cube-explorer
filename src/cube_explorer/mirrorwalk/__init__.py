"""
Mirrorwalk: reproducible symbolic walks + pattern learning + narrative reporting.

Public API:
    from cube_explorer.mirrorwalk import run_mirrorwalk, RunConfig, RunResult
CLI:
    mirrorwalk run ...
    mirrorwalk trends ...
"""
from __future__ import annotations

from .run import run_mirrorwalk
from .schema import RunConfig, RunResult

__all__ = ["RunConfig", "RunResult", "run_mirrorwalk"]
