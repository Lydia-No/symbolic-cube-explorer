"""
Motif mining: n-grams over symbols and derived axis transitions.

Axis extraction assumes hypercube-like moves:
    axis = bit index of (state XOR next_state)
If XOR has multiple bits set, axis = -1 ("non-axial").
"""
from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple


def ngrams(seq: Sequence[object], n: int) -> Iterable[Tuple[object, ...]]:
    if n <= 0 or len(seq) < n:
        return []
    return (tuple(seq[i : i + n]) for i in range(0, len(seq) - n + 1))


def top_ngrams(seq: Sequence[object], n_min: int = 2, n_max: int = 6, top_k: int = 20) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for n in range(n_min, n_max + 1):
        counts = Counter(ngrams(seq, n))
        for gram, c in counts.most_common(top_k):
            results.append({"n": n, "motif": list(gram), "count": int(c)})
    results.sort(key=lambda x: (-int(x["count"]), int(x["n"])))
    return results[:top_k]


def _bit_index_if_single_bit(x: int) -> int:
    if x <= 0 or (x & (x - 1)) != 0:
        return -1
    return x.bit_length() - 1


def axis_sequence_from_path(path: List[int]) -> List[int]:
    axes: List[int] = []
    for a, b in zip(path, path[1:]):
        axes.append(_bit_index_if_single_bit(a ^ b))
    return axes


def top_axis_ngrams(path: List[int], n_min: int = 2, n_max: int = 6, top_k: int = 20) -> List[Dict[str, object]]:
    axes = axis_sequence_from_path(path)
    return top_ngrams(axes, n_min=n_min, n_max=n_max, top_k=top_k)
