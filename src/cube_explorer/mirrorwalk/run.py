"""
Mirrorwalk runner with deep pattern learning.

Includes:
- fixed-symbol execution (execute_sequence)
- adaptive walker (online symbol choice) using novelty + structure + loop avoidance + surprisal
- motif mining (symbol + axis)
- Markov learning + surprisal timeline
- SQLite persistence + cross-run known motif hits
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cube_explorer.core import execute_sequence
from cube_explorer.hypercube import Hypercube

from .learner import MarkovModel, average_finite
from .memory import known_motif_hits, upsert_run
from .metrics import (
    attractor_signature,
    coverage_ratio,
    find_attractors_windowed,
    find_first_loop,
    shannon_entropy,
)
from .motifs import top_axis_ngrams, top_ngrams
from .narrative import build_narrative
from .schema import GrammarInfo, LearningSummary, MotifSummary, RunConfig, RunMetrics, RunResult, utc_now_iso


def _run_id(seed: int, dim: int, steps: int, grammar: str, prompt: Optional[str], walker: str, objective: str) -> str:
    h = hashlib.sha256()
    h.update(f"{seed}|{dim}|{steps}|{grammar}|{walker}|{objective}|{prompt or ''}".encode("utf-8"))
    return h.hexdigest()[:12]


def _load_grammar(grammar_name: str):
    """
    Load grammar object. Expected: cube_explorer.grammars.<name>.GRAMMAR.
    """
    name = grammar_name.strip().lower()
    mod_map = {
        "sefer": "cube_explorer.grammars.sefer",
        "runes": "cube_explorer.grammars.runes",
        "enochian": "cube_explorer.grammars.enochian",
    }
    if name in mod_map:
        mod_path = mod_map[name]
        mod = __import__(mod_path, fromlist=["GRAMMAR"])
        grammar = getattr(mod, "GRAMMAR")
        display = getattr(grammar.metadata(), "display_name", name)
        return grammar, GrammarInfo(name=name, display_name=str(display), source=mod_path)
    raise ValueError(f"Unknown grammar '{grammar_name}'. Known: {sorted(mod_map.keys())}")


def _symbols_from_prompt(prompt: str, steps: int, seed: int, vocab: List[str]) -> List[str]:
    h = hashlib.sha256(prompt.encode("utf-8")).digest()
    derived = int.from_bytes(h[:8], "big") ^ seed
    rng = random.Random(derived)
    return [rng.choice(vocab) for _ in range(steps)]


def _softmax_sample(rng: random.Random, items: List[str], scores: List[float], temperature: float) -> str:
    if len(items) != len(scores) or not items:
        raise ValueError("Invalid softmax inputs")
    t = max(float(temperature), 1e-6)
    m = max(scores)
    exps = [math.exp((s - m) / t) for s in scores]
    total = sum(exps)
    if total <= 0:
        return rng.choice(items)
    r = rng.random() * total
    acc = 0.0
    for item, e in zip(items, exps):
        acc += e
        if acc >= r:
            return item
    return items[-1]


def _safe_vocab(grammar: Any) -> List[str]:
    # For MappingGrammar, _symbol_to_axis exists.
    mapping = getattr(grammar, "_symbol_to_axis", None)
    if isinstance(mapping, dict) and mapping:
        return sorted(mapping.keys())
    return ["A", "B", "C", "D"]


def _adaptive_generate(
    *,
    start: int,
    steps: int,
    seed: int,
    vocab: List[str],
    grammar: Any,
    objective: str,
    markov_order: int,
    loop_window: int,
    temperature: float,
    novelty_power: float,
    structure_power: float,
    loop_penalty: float,
    surprisal_power: float,
) -> Tuple[List[int], List[str], float, int]:
    """
    Generate symbols online, using grammar.apply_symbol to propose next state for each candidate symbol.

    Objective (string) toggles coarse weights:
      - "novelty" increases novelty weight
      - "structure" increases structure weight
      - "avoid-loops" increases loop penalty
      - "surprisal" increases surprisal term
    """
    rng = random.Random(seed)
    path: List[int] = [int(start)]
    chosen: List[str] = []
    score_total = 0.0

    visited_counts: Dict[int, int] = {int(start): 1}
    recent_states: List[int] = [int(start)]

    mm = MarkovModel.create(order=max(1, markov_order))

    # coarse knobs from objective string
    obj = objective.lower().replace(" ", "")
    w_novel = 1.0 + (1.0 if "novelty" in obj else 0.0)
    w_struct = 1.0 + (1.0 if "structure" in obj else 0.0)
    w_loop = 1.0 + (1.0 if "avoid-loops" in obj or "avoidloops" in obj else 0.0)
    w_surp = 1.0 + (1.0 if "surprisal" in obj else 0.0)

    def _structure_reward(seq: List[str], sym: str) -> float:
        """
        Reward repeating short motifs (bigrams/trigrams) without collapsing into trivial loops.
        """
        if not seq:
            return 0.0
        reward = 0.0
        # bigram repeat
        if len(seq) >= 1:
            bigram = (seq[-1], sym)
            # if seen before in seq, reward
            for i in range(0, len(seq) - 1):
                if (seq[i], seq[i + 1]) == bigram:
                    reward += 1.0
                    break
        # trigram repeat
        if len(seq) >= 2:
            tri = (seq[-2], seq[-1], sym)
            for i in range(0, len(seq) - 2):
                if (seq[i], seq[i + 1], seq[i + 2]) == tri:
                    reward += 1.5
                    break
        return reward

    adaptive_decisions = 0

    for _ in range(steps):
        cur = path[-1]

        candidates: List[str] = []
        next_states: List[int] = []
        base_scores: List[float] = []

        # current Markov context
        ctx = tuple(chosen[-mm.order :]) if len(chosen) >= mm.order else None

        for sym in vocab:
            try:
                nxt = int(grammar.apply_symbol(cur, sym))
            except Exception:
                continue

            candidates.append(sym)
            next_states.append(nxt)

            # novelty: prefer less visited
            v = visited_counts.get(nxt, 0)
            novelty = 1.0 / ((1.0 + v) ** max(0.1, novelty_power))

            # loop penalty: penalize landing in recent states
            in_recent = 1.0 if nxt in recent_states[-max(1, loop_window) :] else 0.0
            loop_cost = in_recent * max(0.0, loop_penalty)

            # structure: repeating motifs
            struct = _structure_reward(chosen, sym) ** max(0.1, structure_power)

            # surprisal: prefer moderately surprising moves (not too predictable, not pure noise)
            if ctx is not None:
                s = mm.surprisal(ctx, sym, alpha=1.0)
                if math.isfinite(s):
                    # reward mid-high surprisal; cap to avoid runaway
                    surp_reward = min(s, 6.0) ** max(0.1, surprisal_power)
                else:
                    surp_reward = 0.0
            else:
                surp_reward = 0.0

            score = (
                w_novel * novelty
                + w_struct * struct
                + w_surp * 0.2 * surp_reward
                - w_loop * loop_cost
            )
            base_scores.append(score)

        if not candidates:
            break

        pick = _softmax_sample(rng, candidates, base_scores, temperature=temperature)
        idx = candidates.index(pick)
        nxt_state = next_states[idx]

        # update
        chosen.append(pick)
        path.append(nxt_state)
        visited_counts[nxt_state] = visited_counts.get(nxt_state, 0) + 1
        recent_states.append(nxt_state)
        adaptive_decisions += 1

        # online update markov with newly appended symbol
        if len(chosen) > mm.order:
            mm.update(chosen[-(mm.order + 1) :])

        # scoring for reporting (not used for control)
        score_total += base_scores[idx]

    return path, chosen, score_total, adaptive_decisions


def run_mirrorwalk(
    *,
    out_dir: str,
    space: str,
    dim: int,
    steps: int,
    seed: int,
    start: int,
    grammar_name: str,
    walker: str,
    objective: str,
    symbols: Optional[List[str]],
    prompt: Optional[str],
    memory_path: Optional[str],
    style: str,
    ngram_min: int,
    ngram_max: int,
    markov_order: int,
    write_html: bool,
    # adaptive knobs
    adapt_temperature: float = 0.9,
    loop_window: int = 16,
    novelty_power: float = 1.0,
    structure_power: float = 1.0,
    loop_penalty: float = 1.0,
    surprisal_power: float = 0.6,
) -> RunResult:
    if space.lower() != "hypercube":
        raise ValueError("MVP supports only --space hypercube for now.")

    grammar, ginfo = _load_grammar(grammar_name)
    vocab = _safe_vocab(grammar)

    walker_lc = walker.strip().lower()

    symbols_source = "explicit"
    score: Optional[float] = None

    if symbols:
        used_symbols = symbols[:]
        symbols_source = "explicit"
        path, final_symbols, score_val = execute_sequence(start=start, symbols=used_symbols, grammar=grammar)
        score = float(score_val) if score_val is not None else None

    elif walker_lc in {"adaptive", "learning"}:
        # adaptive ignores prompt-to-sequence and instead treats prompt as seed-mixer for reproducibility
        eff_seed = seed
        if prompt:
            h = hashlib.sha256(prompt.encode("utf-8")).digest()
            eff_seed = seed ^ int.from_bytes(h[:8], "big")

        path, final_symbols, s_total, adaptive_decisions = _adaptive_generate(
            start=start,
            steps=steps,
            seed=eff_seed,
            vocab=vocab,
            grammar=grammar,
            objective=objective,
            markov_order=markov_order,
            loop_window=loop_window,
            temperature=adapt_temperature,
            novelty_power=novelty_power,
            structure_power=structure_power,
            loop_penalty=loop_penalty,
            surprisal_power=surprisal_power,
        )
        symbols_source = "adaptive"
        score = float(s_total)

    else:
        # fixed-symbol generation (prompt/random)
        if prompt:
            used_symbols = _symbols_from_prompt(prompt, steps=steps, seed=seed, vocab=vocab)
            symbols_source = "prompt"
        else:
            rng = random.Random(seed)
            used_symbols = [rng.choice(vocab) for _ in range(steps)]
            symbols_source = "random"

        path, final_symbols, score_val = execute_sequence(start=start, symbols=used_symbols, grammar=grammar)
        score = float(score_val) if score_val is not None else None

    run_id = _run_id(seed, dim, steps, grammar_name, prompt, walker_lc, objective)

    cfg = RunConfig(
        run_id=run_id,
        created_at_utc=utc_now_iso(),
        space=space,
        dim=int(dim),
        steps=int(steps),
        seed=int(seed),
        start=int(start),
        grammar=grammar_name,
        walker=walker_lc,
        objective=objective,
        symbols_source=symbols_source,
        prompt=prompt,
        ngram_min=int(ngram_min),
        ngram_max=int(ngram_max),
        markov_order=int(markov_order),
        memory_path=memory_path,
        style=style,
        write_html=bool(write_html),
        adapt_temperature=float(adapt_temperature),
        loop_window=int(loop_window),
        novelty_power=float(novelty_power),
        structure_power=float(structure_power),
        loop_penalty=float(loop_penalty),
        surprisal_power=float(surprisal_power),
    )

    total_states = 2 ** int(dim)
    cov = coverage_ratio(path, total_states)
    s_entropy = shannon_entropy(path)
    sym_entropy = shannon_entropy(final_symbols)
    loop_found, loop_start, loop_len = find_first_loop(path)

    attractors = find_attractors_windowed(path, window=5, min_repeats=3)
    sig = attractor_signature(attractors)

    sym_grams = top_ngrams(final_symbols, n_min=ngram_min, n_max=ngram_max, top_k=20)
    axis_grams = top_axis_ngrams(path, n_min=ngram_min, n_max=ngram_max, top_k=20)

    mm = MarkovModel.create(order=max(1, markov_order))
    mm.update(final_symbols)
    surprisal = mm.surprisal_timeline(final_symbols)
    avg_s = average_finite(surprisal)

    known_hits = 0
    if memory_path:
        known_hits = known_motif_hits(memory_path, sym_grams, "symbol")

    metrics = RunMetrics(
        path_len=len(path),
        unique_states=len(set(path)),
        coverage_ratio=float(cov),
        state_entropy=float(s_entropy),
        symbol_entropy=float(sym_entropy),
        avg_surprisal=float(avg_s),
        loop_found=bool(loop_found),
        loop_start=loop_start,
        loop_len=loop_len,
        attractor_signature=sig,
    )

    motifs = MotifSummary(symbol_ngrams=sym_grams, axis_ngrams=axis_grams)

    adaptive_decisions = len(final_symbols) if symbols_source == "adaptive" else 0

    learning = LearningSummary(
        markov_order=int(markov_order),
        context_counts=len(mm.context_counts),
        transition_counts=sum(len(v) for v in mm.transition_counts.values()),
        motif_hits=len(sym_grams),
        known_motif_hits=int(known_hits),
        adaptive_decisions=int(adaptive_decisions),
        adaptive_vocab=int(len(vocab)),
    )

    result = RunResult(
        config=cfg,
        grammar_info=ginfo,
        symbols=list(final_symbols),
        path=list(path),
        score=score,
        metrics=metrics,
        motifs=motifs,
        surprisal=list(surprisal),
        learning=learning,
    )

    if memory_path:
        upsert_run(memory_path, result)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    (out / "run.json").write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    narrative, why = build_narrative(result)
    report = _render_report_md(result, narrative=narrative, why=why)
    (out / "report.md").write_text(report, encoding="utf-8")

    if write_html:
        _write_walk_html(out / "walk.html", result)

    return result


def _render_report_md(result: RunResult, *, narrative: str, why: List[str]) -> str:
    m = result.metrics
    lines: List[str] = []
    lines.append(f"# Mirrorwalk Report — {result.config.run_id}")
    lines.append("")
    lines.append("## Mechanics")
    lines.append(f"- Grammar: **{result.grammar_info.display_name}** (`{result.grammar_info.source}`)")
    lines.append(f"- Space: **{result.config.space}** (dim={result.config.dim}, states={2**result.config.dim})")
    lines.append(f"- Steps: **{result.config.steps}** | Start: **{result.config.start}** | Seed: **{result.config.seed}**")
    lines.append(f"- Walker: **{result.config.walker}** | Objective: **{result.config.objective}**")
    lines.append(f"- Symbols source: **{result.config.symbols_source}**")
    lines.append(f"- Score: **{result.score}**")
    lines.append("")
    lines.append("### Metrics")
    lines.append(f"- Path length: {m.path_len}")
    lines.append(f"- Unique states: {m.unique_states}")
    lines.append(f"- Coverage ratio: {m.coverage_ratio:.3f}")
    lines.append(f"- State entropy: {m.state_entropy:.3f}")
    lines.append(f"- Symbol entropy: {m.symbol_entropy:.3f}")
    lines.append(f"- Avg surprisal (Markov): {m.avg_surprisal:.3f}")
    lines.append(f"- Loop found: {m.loop_found} (start={m.loop_start}, len={m.loop_len})")
    lines.append(f"- Attractor signature: {m.attractor_signature}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append(narrative)
    lines.append("")
    lines.append("### Why this interpretation")
    if why:
        for w in why:
            lines.append(f"- {w}")
    else:
        lines.append("- No dominant triggers; interpretation is intentionally minimal.")
    lines.append("")
    lines.append("## Pattern Learning")
    lines.append(f"- Markov order: {result.learning.markov_order}")
    lines.append(f"- Contexts learned: {result.learning.context_counts}")
    lines.append(f"- Transitions learned: {result.learning.transition_counts}")
    lines.append(f"- Motifs found (symbol n-grams): {result.learning.motif_hits}")
    lines.append(f"- Known motif hits (memory): {result.learning.known_motif_hits}")
    lines.append(f"- Adaptive decisions: {result.learning.adaptive_decisions} (vocab={result.learning.adaptive_vocab})")
    lines.append("")
    lines.append("## Top Motifs")
    if result.motifs.symbol_ngrams:
        lines.append("### Symbol n-grams")
        for item in result.motifs.symbol_ngrams[:10]:
            lines.append(f"- n={item['n']} count={item['count']} motif={item['motif']}")
    if result.motifs.axis_ngrams:
        lines.append("")
        lines.append("### Axis n-grams (bit flip indices)")
        for item in result.motifs.axis_ngrams[:10]:
            lines.append(f"- n={item['n']} count={item['count']} motif={item['motif']}")
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("Everything needed to reproduce this run is in `run.json` (seed, grammar, dim, symbols).")
    lines.append("")
    return "\n".join(lines)


def _write_walk_html(path: Path, result: RunResult) -> None:
    escaped = json.dumps(result.path)
    html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Mirrorwalk {result.config.run_id}</title></head>
<body>
<h1>Mirrorwalk {result.config.run_id}</h1>
<p>Path length: {len(result.path)} | Unique: {len(set(result.path))}</p>
<pre id="data"></pre>
<script>
const path = {escaped};
document.getElementById("data").textContent = JSON.stringify({{path}}, null, 2);
</script>
</body>
</html>"""
    path.write_text(html, encoding="utf-8")
