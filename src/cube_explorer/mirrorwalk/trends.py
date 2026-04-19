"""
Trends report over Mirrorwalk SQLite memory.

Outputs Markdown that summarizes:
- recent runs
- entropy/coverage/surprisal drift
- attractor signature distribution
- motif leaderboards (symbol + axis)

This is intentionally explainable, not ML-heavy.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .memory import list_runs, motif_leaderboard


def render_trends_md(
    *,
    memory_path: str,
    grammar: Optional[str],
    limit: int,
    motif_n: Optional[int],
) -> str:
    runs = list_runs(memory_path, grammar=grammar, limit=limit)

    title = "Mirrorwalk Trends"
    if grammar:
        title += f" — {grammar}"

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    if not runs:
        lines.append("No runs found in memory.")
        return "\n".join(lines)

    lines.append(f"- Runs shown: {len(runs)} (most recent first)")
    lines.append("")
    lines.append("## Recent runs")
    for r in runs[: min(10, len(runs))]:
        lines.append(
            f"- `{r['run_id']}` {r['created_at_utc']} "
            f"(dim={r['dim']}, steps={r['steps']}, walker={r['walker']}, obj={r['objective']}) "
            f"| H_state={r['state_entropy']:.3f} H_sym={r['symbol_entropy']:.3f} "
            f"cov={r['coverage_ratio']:.3f} surprisal={r['avg_surprisal']:.3f}"
        )
    lines.append("")

    # simple drift view
    lines.append("## Drift (older → newer)")
    rev = list(reversed(runs))
    def _series(key: str) -> List[float]:
        return [float(x[key]) for x in rev]

    hs = _series("state_entropy")
    hy = _series("symbol_entropy")
    cov = _series("coverage_ratio")
    sp = _series("avg_surprisal")

    lines.append(f"- State entropy: {hs[0]:.3f} → {hs[-1]:.3f}")
    lines.append(f"- Symbol entropy: {hy[0]:.3f} → {hy[-1]:.3f}")
    lines.append(f"- Coverage ratio: {cov[0]:.3f} → {cov[-1]:.3f}")
    lines.append(f"- Avg surprisal: {sp[0]:.3f} → {sp[-1]:.3f}")
    lines.append("")

    # attractor signature distribution
    lines.append("## Attractor signatures (windowed)")
    sig_counts: Dict[str, int] = {}
    for r in runs:
        sig = r.get("attractor_signature") or {}
        for k, v in sig.items():
            sig_counts[k] = sig_counts.get(k, 0) + int(v)
    if not sig_counts:
        lines.append("- None recorded.")
    else:
        for k in sorted(sig_counts.keys(), key=lambda x: int(x) if x.isdigit() else 999999):
            lines.append(f"- window={k}: total={sig_counts[k]}")
    lines.append("")

    # motifs
    lines.append("## Motif leaderboards")
    lines.append("")
    sym = motif_leaderboard(memory_path, grammar=grammar, motif_type="symbol", n=motif_n, limit=20)
    ax = motif_leaderboard(memory_path, grammar=grammar, motif_type="axis", n=motif_n, limit=20)

    lines.append("### Symbol motifs")
    if not sym:
        lines.append("- None.")
    else:
        for m in sym[:10]:
            lines.append(f"- n={m['n']} runs={m['run_count']} total={m['total_count']} motif={m['motif']}")
    lines.append("")
    lines.append("### Axis motifs")
    if not ax:
        lines.append("- None.")
    else:
        for m in ax[:10]:
            lines.append(f"- n={m['n']} runs={m['run_count']} total={m['total_count']} motif={m['motif']}")
    lines.append("")

    lines.append("## Notes")
    lines.append("- Motifs are hashed and counted across runs; this supports cross-run pattern learning.")
    lines.append("- Drift is computed from the oldest of the selected runs to the newest.")
    lines.append("")
    return "\n".join(lines)
