import math
from collections import Counter

def shannon_entropy(sequence):
    counts = Counter(sequence)
    total = sum(counts.values())

    probs = [c / total for c in counts.values()]
    return -sum(p * math.log(p + 1e-12) for p in probs)
