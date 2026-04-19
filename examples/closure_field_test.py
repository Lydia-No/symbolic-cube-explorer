import random
from collections import Counter


AXES = [1, 2, 4, 8]


def random_sequence(length=8):
    return [random.choice(AXES) for _ in range(length)]


def distance_to_closure(seq):
    counts = Counter(seq)

    # count how many axes are unpaired (odd occurrences)
    imbalance = sum(1 for v in counts.values() if v % 2 != 0)

    return imbalance


def repair_cost(seq):
    # minimal number of steps to repair = imbalance
    return distance_to_closure(seq)


def is_closed(seq):
    return distance_to_closure(seq) == 0


def run(samples=1000):
    print("\nCLOSURE FIELD TEST\n")

    histogram = {}

    for _ in range(samples):
        seq = random_sequence()
        d = distance_to_closure(seq)

        histogram[d] = histogram.get(d, 0) + 1

    print("--- DISTRIBUTION ---\n")

    for d in sorted(histogram):
        count = histogram[d]
        pct = 100 * count / samples
        print(f"distance {d}: {count} ({pct:.2f}%)")

    print("\n--- EXAMPLES ---\n")

    for _ in range(10):
        seq = random_sequence()
        d = distance_to_closure(seq)

        print(f"{seq} → distance={d}")


if __name__ == "__main__":
    run()
