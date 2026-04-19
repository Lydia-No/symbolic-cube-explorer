from collections import Counter

# observed high-frequency forbidden states
patterns = ['0000', '0011', '0111', '1101', '1111']


def classify(state):
    ones = state.count("1")

    if ones == 0:
        return "ground"
    elif ones == 1:
        return "single"
    elif ones == 2:
        return "pair"
    elif ones == 3:
        return "triple"
    else:
        return "full"


def main():
    categories = Counter()

    for s in patterns:
        categories[classify(s)] += 1

    print("Pattern classes:")
    for k, v in categories.items():
        print(k, ":", v)


if __name__ == "__main__":
    main()
