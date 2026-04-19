"""
Learning patterns: Markov model over symbols with surprisal timeline.
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, Iterable, List, Sequence, Tuple


Context = Tuple[str, ...]


@dataclass
class MarkovModel:
    order: int
    context_counts: Counter
    transition_counts: DefaultDict[Context, Counter]

    @classmethod
    def create(cls, order: int) -> "MarkovModel":
        if order < 1:
            raise ValueError("Markov order must be >= 1")
        return cls(order=order, context_counts=Counter(), transition_counts=defaultdict(Counter))

    def update(self, symbols: Sequence[str]) -> None:
        if len(symbols) <= self.order:
            return
        for i in range(self.order, len(symbols)):
            ctx = tuple(symbols[i - self.order : i])
            nxt = symbols[i]
            self.context_counts[ctx] += 1
            self.transition_counts[ctx][nxt] += 1

    def prob(self, ctx: Context, nxt: str, alpha: float = 1.0) -> float:
        counts = self.transition_counts.get(ctx)
        if not counts:
            return 0.0
        total = sum(counts.values())
        vocab = max(len(counts), 1)
        return (counts.get(nxt, 0) + alpha) / (total + alpha * vocab)

    def surprisal(self, ctx: Context, nxt: str, alpha: float = 1.0) -> float:
        p = self.prob(ctx, nxt, alpha=alpha)
        if p <= 0:
            return float("inf")
        return -math.log2(p)

    def surprisal_timeline(self, symbols: Sequence[str], alpha: float = 1.0) -> List[float]:
        if len(symbols) <= self.order:
            return []
        out: List[float] = []
        for i in range(self.order, len(symbols)):
            ctx = tuple(symbols[i - self.order : i])
            out.append(self.surprisal(ctx, symbols[i], alpha=alpha))
        return out


def average_finite(values: Iterable[float]) -> float:
    vals = [v for v in values if math.isfinite(v)]
    if not vals:
        return 0.0
    return sum(vals) / len(vals)
