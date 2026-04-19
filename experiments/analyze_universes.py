import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from collections import Counter

# paste your best results manually here for now
top_universes = [
    {'0000', '1101'},
    {'1100', '1001'},
    {'0011', '1111'},
    {'0010', '0101'},
    {'0011', '0110'},
]


def bit_patterns(states):
    patterns = Counter()

    for s in states:
        ones = s.count("1")
        patterns[f"{ones}_ones"] += 1

    return patterns


def main():
    total = Counter()

    for u in top_universes:
        p = bit_patterns(u)
        total.update(p)

    print("Pattern distribution:")
    for k, v in total.items():
        print(k, ":", v)


if __name__ == "__main__":
    main()
