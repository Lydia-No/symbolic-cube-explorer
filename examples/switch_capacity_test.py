import random
from collections import defaultdict


AXES = [1, 2, 4, 8]  # Q4, but doesn't really matter now


def random_sequence(length=8):
    return [random.choice(AXES) for _ in range(length)]


def count_switches(seq):
    switches = 0
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]:
            switches += 1
    return switches


def is_lineage_preserved(seq):
    if len(seq) < 2:
        return False

    if seq[0] != seq[-1]:
        return False

    if len(set(seq)) == 1:
        return False

    return True


def score_sequence(seq):
    score = 0

    if seq == seq[::-1]:
        score += 5

    if len(set(seq)) < len(seq):
        score += 2

    if seq[0] == seq[-1]:
        score += 3

    return score


def run(total=20000, length=8):
    print("\nSWITCH CAPACITY SCAN\n")

    stats = defaultdict(lambda: {"count": 0, "lineage": 0, "high_score": 0})
    best = {}

    for _ in range(total):
        seq = random_sequence(length)
        switches = count_switches(seq)
        lineage = is_lineage_preserved(seq)
        score = score_sequence(seq)

        stats[switches]["count"] += 1

        if lineage:
            stats[switches]["lineage"] += 1

        if score >= 10:
            stats[switches]["high_score"] += 1

        if switches not in best or score > best[switches]["score"]:
            best[switches] = {"seq": seq, "score": score}

    print("--- BY SWITCH COUNT ---\n")

    for s in sorted(stats):
        count = stats[s]["count"]
        lineage = stats[s]["lineage"]
        high_score = stats[s]["high_score"]

        lineage_pct = 100 * lineage / count if count else 0
        high_score_pct = 100 * high_score / count if count else 0

        print(f"Switches {s}:")
        print(f"  total: {count}")
        print(f"  lineage preserved: {lineage} ({lineage_pct:.2f}%)")
        print(f"  score >= 10: {high_score} ({high_score_pct:.2f}%)")
        print(f"  best example: {best[s]['seq']} | score={best[s]['score']}")
        print()


if __name__ == "__main__":
    run()
