import random
from collections import defaultdict


AXES_Q4 = [1, 2, 4, 8]


def random_sequence(length=8):
    return [random.choice(AXES_Q4) for _ in range(length)]


def score_sequence(seq):
    score = 0

    if seq == seq[::-1]:
        score += 5

    if len(set(seq)) < len(seq):
        score += 2

    if seq[0] == seq[-1]:
        score += 3

    return score


def count_axis_switches(seq):
    if not seq:
        return 0

    switches = 0
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]:
            switches += 1
    return switches


def is_lineage_preserved(seq):
    """
    Same rule as before:
    - start and end match
    - not trivial single-axis repetition
    """
    if len(seq) < 2:
        return False

    if seq[0] != seq[-1]:
        return False

    if len(set(seq)) == 1:
        return False

    return True


def variation_depth(seq):
    """
    Same crude depth metric:
    switches + distinct_axes - 1
    """
    return count_axis_switches(seq) + (len(set(seq)) - 1)


def classify(seq):
    score = score_sequence(seq)
    lineage = is_lineage_preserved(seq)
    depth = variation_depth(seq)
    switches = count_axis_switches(seq)

    return {
        "seq": seq,
        "score": score,
        "lineage": lineage,
        "depth": depth,
        "switches": switches,
    }


def run(total=20000, length=8):
    print("\nQ4 LINEAGE THRESHOLD SCAN\n")

    stats = defaultdict(lambda: {"count": 0, "lineage": 0, "high_score": 0})
    best_examples = {}

    for _ in range(total):
        seq = random_sequence(length)
        info = classify(seq)
        depth = info["depth"]

        stats[depth]["count"] += 1

        if info["lineage"]:
            stats[depth]["lineage"] += 1

        if info["score"] >= 10:
            stats[depth]["high_score"] += 1

        if depth not in best_examples or info["score"] > best_examples[depth]["score"]:
            best_examples[depth] = info

    print("--- BY VARIATION DEPTH ---\n")

    for depth in sorted(stats):
        count = stats[depth]["count"]
        lineage = stats[depth]["lineage"]
        high_score = stats[depth]["high_score"]

        lineage_pct = 100 * lineage / count if count else 0
        high_score_pct = 100 * high_score / count if count else 0

        print(f"Depth {depth}:")
        print(f"  total: {count}")
        print(f"  lineage preserved: {lineage} ({lineage_pct:.2f}%)")
        print(f"  score >= 10: {high_score} ({high_score_pct:.2f}%)")
        print(f"  best example: {best_examples[depth]['seq']} | score={best_examples[depth]['score']}")
        print()

    print("--- TOP LINEAGE EXAMPLES ---\n")

    lineage_examples = []
    for depth in best_examples:
        info = best_examples[depth]
        if info["lineage"]:
            lineage_examples.append(info)

    lineage_examples.sort(key=lambda x: (-x["score"], -x["depth"], x["seq"]))

    for info in lineage_examples[:12]:
        print(
            f"seq={info['seq']} | score={info['score']} | "
            f"depth={info['depth']} | switches={info['switches']}"
        )


if __name__ == "__main__":
    run()
