"""
Metrics for Mirrorwalk: entropy, coverage, loop and attractor signatures.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


def shannon_entropy(seq: Iterable[object]) -> float:
    items = list(seq)
    n = len(items)
    if n == 0:
        return 0.0
    counts = Counter(items)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def coverage_ratio(path: List[int], total_states: int) -> float:
    if total_states <= 0:
        return 0.0
    return len(set(path)) / float(total_states)


def find_first_loop(path: List[int]) -> Tuple[bool, Optional[int], Optional[int]]:
    seen: Dict[int, int] = {}
    for i, s in enumerate(path):
        if s in seen:
            start = seen[s]
            return True, start, i - start
        seen[s] = i
    return False, None, None


@dataclass(frozen=True)
class Attractor:
    motif: Tuple[int, ...]
    count: int


def find_attractors_windowed(path: List[int], window: int = 5, min_repeats: int = 3) -> List[Attractor]:
    if window <= 0 or len(path) < window:
        return []
    windows = [tuple(path[i : i + window]) for i in range(0, len(path) - window + 1)]
    counts = Counter(windows)
    found = [Attractor(motif=w, count=c) for w, c in counts.items() if c >= min_repeats]
    found.sort(key=lambda a: (-a.count, a.motif))
    return found


def attractor_signature(attractors: List[Attractor]) -> Dict[str, int]:
    sig: Dict[str, int] = {}
    for a in attractors:
        key = str(len(a.motif))
        sig[key] = sig.get(key, 0) + 1
    return sig
