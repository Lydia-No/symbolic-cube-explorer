from collections import Counter


def find_attractors(trajectory, window=5, min_repeats=2):
    seen = Counter()
    attractors = []

    for i in range(len(trajectory) - window):
        segment = tuple(trajectory[i:i+window])
        seen[segment] += 1

    for segment, count in seen.items():
        if count >= min_repeats:
            attractors.append((segment, count))

    attractors.sort(key=lambda x: x[1], reverse=True)
    return attractors


def attractor_signature(attractors):
    """
    Compress attractors into a structural signature
    """
    signature = Counter()

    for segment, count in attractors:
        # measure bit transitions inside attractor
        transitions = 0
        for i in range(len(segment) - 1):
            a = segment[i]
            b = segment[i + 1]

            # Hamming distance
            diff = sum(1 for x, y in zip(a, b) if x != y)
            transitions += diff

        signature[transitions] += count

    return dict(signature)
