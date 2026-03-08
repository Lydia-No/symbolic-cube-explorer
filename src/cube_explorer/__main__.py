from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import List, Optional, Sequence

from .core import CubeGraph, SymbolicWalker, concept_seed, execute_sequence
from .grammars import get_grammar, list_grammars


@dataclass(frozen=True)
class RunResult:
    grammar: str
    concept: str
    start: int
    path: List[int]
    sequence: List[str]
    score: int


def _parse_symbols(s: str) -> List[str]:
    # allow: "א מ ש" or "א,מ,ש" or "א|מ|ש"
    raw = s.replace(",", " ").replace("|", " ").strip()
    return [tok for tok in raw.split() if tok]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cube_explorer", description="Execute symbol programs on Q3.")
    p.add_argument("--list-grammars", action="store_true", help="List available grammars and exit.")
    p.add_argument("--grammar", type=str, default="sefer", help="Grammar plugin name (default: sefer).")
    p.add_argument("--concept", type=str, default="collective intelligence", help="Seed concept.")
    p.add_argument("--symbols", type=str, default="", help='Symbol program, e.g. "א מ ש א מ ש".')
    p.add_argument("--steps", type=int, default=6, help="If --symbols empty, auto-generate steps from grammar symbols.")
    p.add_argument("--json", action="store_true", help="Print JSON output.")
    p.add_argument("--plot", action="store_true", help="Show Plotly figure.")
    p.add_argument("--html", type=str, default=None, help="Write Plotly HTML to this path.")
    return p


def _auto_symbols(grammar_name: str, steps: int) -> List[str]:
    g = get_grammar(grammar_name)
    syms = list(g.symbols())
    if not syms:
        raise ValueError(f"Grammar {grammar_name} has no symbols()")
    return [syms[i % len(syms)] for i in range(steps)]


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)

    if args.list_grammars:
        print("\n".join(list_grammars()))
        return 0

    grammar = get_grammar(args.grammar)
    cube = CubeGraph()
    walker = SymbolicWalker(cube=cube, grammar=grammar)

    symbols = _parse_symbols(args.symbols) if args.symbols else _auto_symbols(args.grammar, args.steps)

    start = concept_seed(args.concept, dims=cube.dims)
    path, seq, score = execute_sequence(start=start, symbols=symbols, grammar=grammar)

    result = RunResult(
        grammar=args.grammar,
        concept=args.concept,
        start=start,
        path=path,
        sequence=seq,
        score=score,
    )

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print("Grammar:", args.grammar)
        print("Concept:", args.concept)
        print("Start:", start)
        print("Path:", path)
        print("Sequence:", " ".join(seq))
        print("Score:", score)

    if args.plot or args.html:
        from .visualization import plot_cube_walk
        fig = plot_cube_walk(path)
        if args.html:
            fig.write_html(args.html)
            print(f"Wrote {args.html}")
        if args.plot:
            fig.show()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
