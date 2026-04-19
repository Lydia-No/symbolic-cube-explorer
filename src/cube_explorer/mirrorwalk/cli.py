"""
Mirrorwalk CLI.

Commands:
  mirrorwalk run ...
  mirrorwalk trends --memory ~/.mirrorwalk/memory.sqlite
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List, Optional

from .run import run_mirrorwalk
from .trends import render_trends_md


def _parse_symbols(s: str) -> List[str]:
    raw = s.replace(",", " ").split()
    return [x.strip() for x in raw if x.strip()]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mirrorwalk")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run a mirrorwalk and write run.json/report.md.")
    run.add_argument("--space", default="hypercube", choices=["hypercube"])
    run.add_argument("--dim", type=int, default=6)
    run.add_argument("--steps", type=int, default=512)
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--start", type=int, default=0)
    run.add_argument("--grammar", default="sefer", help="sefer|runes|enochian")
    run.add_argument("--walker", default="adaptive", help="random|biased|adaptive|learning")
    run.add_argument("--objective", default="novelty+structure")
    run.add_argument("--symbols", default=None, help="Explicit symbol sequence (comma/space separated).")
    run.add_argument("--prompt", default=None, help="Prompt to deterministically generate symbols.")
    run.add_argument("--memory", default=None, help="SQLite memory path, e.g. ~/.mirrorwalk/memory.sqlite")
    run.add_argument("--style", default="mythic", choices=["mythic", "jungian", "cyber"])
    run.add_argument("--out", default=None, help="Output directory. Default: ./runs/<run_id>")
    run.add_argument("--ngram-min", type=int, default=2)
    run.add_argument("--ngram-max", type=int, default=6)
    run.add_argument("--markov-order", type=int, default=2)
    run.add_argument("--html", action="store_true", help="Write walk.html (minimal).")

    # adaptive knobs
    run.add_argument("--adapt-temp", type=float, default=0.9)
    run.add_argument("--loop-window", type=int, default=16)
    run.add_argument("--novelty-power", type=float, default=1.0)
    run.add_argument("--structure-power", type=float, default=1.0)
    run.add_argument("--loop-penalty", type=float, default=1.0)
    run.add_argument("--surprisal-power", type=float, default=0.6)

    tr = sub.add_parser("trends", help="Summarize cross-run memory as Markdown.")
    tr.add_argument("--memory", required=True, help="SQLite memory path.")
    tr.add_argument("--grammar", default=None, help="Filter by grammar.")
    tr.add_argument("--limit", type=int, default=50, help="Number of runs to include.")
    tr.add_argument("--motif-n", type=int, default=None, help="Filter motifs by n.")
    tr.add_argument("--out", default=None, help="Write to file instead of stdout.")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    p = build_parser()
    args = p.parse_args(argv)

    if args.cmd == "run":
        symbols = _parse_symbols(args.symbols) if args.symbols else None

        memory = os.path.expanduser(args.memory) if args.memory else None
        out_dir = os.path.expanduser(args.out) if args.out else None

        tmp_out = out_dir or "./runs/_tmp"
        result = run_mirrorwalk(
            out_dir=tmp_out,
            space=args.space,
            dim=args.dim,
            steps=args.steps,
            seed=args.seed,
            start=args.start,
            grammar_name=args.grammar,
            walker=args.walker,
            objective=args.objective,
            symbols=symbols,
            prompt=args.prompt,
            memory_path=memory,
            style=args.style,
            ngram_min=args.ngram_min,
            ngram_max=args.ngram_max,
            markov_order=args.markov_order,
            write_html=args.html,
            adapt_temperature=args.adapt_temp,
            loop_window=args.loop_window,
            novelty_power=args.novelty_power,
            structure_power=args.structure_power,
            loop_penalty=args.loop_penalty,
            surprisal_power=args.surprisal_power,
        )

        if not out_dir:
            final = Path("./runs") / result.config.run_id
            final.parent.mkdir(parents=True, exist_ok=True)
            tmp = Path(tmp_out)
            if tmp.exists():
                if final.exists():
                    raise SystemExit(f"Output path exists: {final}")
                tmp.rename(final)
            print(str(final))
        else:
            print(str(Path(out_dir)))
        return 0

    if args.cmd == "trends":
        memory = os.path.expanduser(args.memory)
        md = render_trends_md(memory_path=memory, grammar=args.grammar, limit=args.limit, motif_n=args.motif_n)
        if args.out:
            out_path = Path(os.path.expanduser(args.out))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8")
            print(str(out_path))
        else:
            print(md)
        return 0

    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
