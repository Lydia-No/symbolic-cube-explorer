"""
Schema and serialization helpers for Mirrorwalk outputs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class GrammarInfo:
    name: str
    display_name: str
    source: str  # import path or "custom"
    notes: Optional[str] = None


@dataclass(frozen=True)
class RunConfig:
    run_id: str
    created_at_utc: str
    space: str
    dim: int
    steps: int
    seed: int
    start: int
    grammar: str
    walker: str
    objective: str
    symbols_source: str  # "explicit" | "prompt" | "random" | "adaptive"
    prompt: Optional[str] = None
    ngram_min: int = 2
    ngram_max: int = 6
    markov_order: int = 2
    memory_path: Optional[str] = None
    style: str = "mythic"
    write_html: bool = False

    # adaptive knobs
    adapt_temperature: float = 0.9
    loop_window: int = 16
    novelty_power: float = 1.0
    structure_power: float = 1.0
    loop_penalty: float = 1.0
    surprisal_power: float = 0.6


@dataclass
class RunMetrics:
    path_len: int
    unique_states: int
    coverage_ratio: float
    state_entropy: float
    symbol_entropy: float
    avg_surprisal: float
    loop_found: bool
    loop_start: Optional[int] = None
    loop_len: Optional[int] = None
    attractor_signature: Dict[str, int] = field(default_factory=dict)


@dataclass
class LearningSummary:
    markov_order: int
    context_counts: int
    transition_counts: int
    motif_hits: int
    known_motif_hits: int
    adaptive_decisions: int
    adaptive_vocab: int


@dataclass
class MotifSummary:
    symbol_ngrams: List[Dict[str, Any]]
    axis_ngrams: List[Dict[str, Any]]


@dataclass
class RunResult:
    config: RunConfig
    grammar_info: GrammarInfo
    symbols: List[str]
    path: List[int]
    score: Optional[float]
    metrics: RunMetrics
    motifs: MotifSummary
    surprisal: List[float]
    learning: LearningSummary
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
