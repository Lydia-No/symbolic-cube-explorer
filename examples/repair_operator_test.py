def repair_sequence(seq):
    """
    Minimal closure repair:
    append reverse of sequence
    """
    return seq + seq[::-1]


def is_closed(seq):
    return seq[0] == seq[-1]


def run():
    examples = [
        [2, 1, 4, 8],
        [1, 2, 2],
        [4, 1, 2, 8, 2],
    ]

    print("\nREPAIR TEST\n")

    for seq in examples:
        repaired = repair_sequence(seq)

        print("Original:", seq)
        print("Repaired:", repaired)
        print("Closed:", is_closed(repaired))
        print("-" * 30)


if __name__ == "__main__":
    run()
