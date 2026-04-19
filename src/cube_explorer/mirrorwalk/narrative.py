"""
Narrative layer: mythic / jungian / cyber.

Rules:
- never predictive/medical/financial claims
- always map lines back to measurable signals in "why"
"""
from __future__ import annotations

from typing import List, Tuple

from .schema import RunResult


def build_narrative(result: RunResult) -> Tuple[str, List[str]]:
    style = (result.config.style or "mythic").lower()
    if style == "jungian":
        return _jungian(result)
    if style == "cyber":
        return _cyber(result)
    return _mythic(result)


def _mythic(r: RunResult) -> Tuple[str, List[str]]:
    m = r.metrics
    lines: List[str] = []
    why: List[str] = []

    if m.loop_found and m.loop_len:
        lines.append(f"A returning pattern appears (cycle length {m.loop_len}).")
        why.append(f"Loop detected at index {m.loop_start} with length {m.loop_len}.")

    if m.state_entropy < 1.5:
        lines.append("Repetition thickens into ritual: structure is dominant.")
        why.append(f"Low state entropy ({m.state_entropy:.3f}).")
    elif m.state_entropy > 2.7:
        lines.append("The walk keeps opening doors: novelty remains high.")
        why.append(f"High state entropy ({m.state_entropy:.3f}).")

    top_motif = r.motifs.symbol_ngrams[0] if r.motifs.symbol_ngrams else None
    if top_motif:
        lines.append(f"A refrain repeats: {top_motif['motif']} (x{top_motif['count']}).")
        why.append(f"Top symbol n-gram n={top_motif['n']} count={top_motif['count']}.")

    if r.learning.known_motif_hits > 0:
        lines.append("Some motifs feel familiar: memory recognizes previous echoes.")
        why.append(f"Known motif hits in memory: {r.learning.known_motif_hits}.")

    return "\n".join(lines) if lines else "A quiet run: patterns exist but don’t dominate.", why


def _jungian(r: RunResult) -> Tuple[str, List[str]]:
    m = r.metrics
    lines: List[str] = []
    why: List[str] = []

    if m.loop_found and m.loop_len:
        lines.append(f"A compulsion-loop emerges (len {m.loop_len}).")
        why.append(f"Loop detected at index {m.loop_start} with length {m.loop_len}.")

    if m.avg_surprisal > 2.5:
        lines.append("Expectation breaks repeatedly: disruption creates reflection opportunities.")
        why.append(f"Average surprisal {m.avg_surprisal:.3f} is high.")

    if m.coverage_ratio < 0.15:
        lines.append("The system stays local: familiar territory dominates.")
        why.append(f"Coverage ratio {m.coverage_ratio:.3f} is low.")

    return "\n".join(lines) if lines else "Stable run: structure outweighs disruption.", why


def _cyber(r: RunResult) -> Tuple[str, List[str]]:
    m = r.metrics
    lines: List[str] = []
    why: List[str] = []

    if m.loop_found and m.loop_len:
        lines.append(f"Daemon loop detected (cycle {m.loop_len}).")
        why.append(f"Loop detected at index {m.loop_start} with length {m.loop_len}.")

    if m.avg_surprisal > 2.5:
        lines.append("Interrupt spikes: the walker injects rare transitions.")
        why.append(f"Average surprisal {m.avg_surprisal:.3f}.")

    if m.attractor_signature:
        lines.append(f"Attractor signature online: {m.attractor_signature}.")
        why.append(f"Windowed attractors found: {m.attractor_signature}.")

    return "\n".join(lines) if lines else "Low-noise trace: no dominant anomalies.", why
