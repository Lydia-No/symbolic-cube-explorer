import argparse
from cube_explorer.hypercube import Hypercube


def run(dim, steps):

    cube = Hypercube(dim)

    seq = cube.random_walk(steps)

    print("\nSymbolic sequence:\n")

    print(" ".join(seq))


def main():

    parser = argparse.ArgumentParser(
        description="Symbolic Cube Explorer CLI"
    )

    parser.add_argument(
        "command",
        choices=["run"],
        help="command to execute"
    )

    parser.add_argument(
        "--dim",
        type=int,
        default=4,
        help="hypercube dimension"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=50,
        help="random walk length"
    )

    args = parser.parse_args()

    if args.command == "run":
        run(args.dim, args.steps)


if __name__ == "__main__":
    main()
