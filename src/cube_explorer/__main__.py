import argparse

from cube_explorer.hypercube import Hypercube
from cube_explorer.analysis import entropy
from cube_explorer.attractors import find_symbol_cycles
from cube_explorer.symmetry import symmetry_score
from cube_explorer.experiments import entropy_curve


# -----------------------------
# Command implementations
# -----------------------------

def cmd_run(args):

    cube = Hypercube(args.dim)
    seq = cube.random_walk(args.steps)

    print("\nSymbolic sequence:\n")
    print(" ".join(seq))


def cmd_entropy(args):

    cube = Hypercube(args.dim)
    seq = cube.random_walk(args.steps)

    H = entropy(seq)

    print(f"\nHypercube Q{args.dim}")
    print(f"Steps: {args.steps}")
    print(f"Entropy: {H:.6f}\n")


def cmd_attractors(args):

    cube = Hypercube(args.dim)
    seq = cube.random_walk(args.steps)

    cycles = find_symbol_cycles(seq)

    print(f"\nHypercube Q{args.dim}")
    print("\nTop attractor cycles:\n")

    for c in cycles[:10]:
        print(f"{c['cycle']} (len={c['length']}, count={c['occurrences']})")


def cmd_scan(args):

    start, end = args.dims

    print("\nEntropy scan across hypercube dimensions\n")

    for d in range(start, end + 1):

        cube = Hypercube(d)
        seq = cube.random_walk(args.steps)

        H = entropy(seq)

        print(f"Q{d}: entropy = {H:.6f}")


def cmd_symmetry(args):

    cube = Hypercube(args.dim)
    seq = cube.random_walk(args.steps)

    score, counts = symmetry_score(seq)

    print(f"\nHypercube Q{args.dim}")
    print("\nSymbol frequencies:\n")

    for s, c in sorted(counts.items()):
        print(f"{s}: {c}")

    print(f"\nSymmetry score: {score:.6f}\n")


def cmd_entropy_curve(args):

    entropy_curve(
        start=args.start,
        end=args.end,
        steps=args.steps
    )


# -----------------------------
# CLI
# -----------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Symbolic Cube Explorer"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # run
    run_cmd = sub.add_parser("run", help="generate symbolic walk")
    run_cmd.add_argument("--dim", type=int, default=4)
    run_cmd.add_argument("--steps", type=int, default=50)
    run_cmd.set_defaults(func=cmd_run)

    # entropy
    entropy_cmd = sub.add_parser("entropy", help="compute entropy")
    entropy_cmd.add_argument("--dim", type=int, default=4)
    entropy_cmd.add_argument("--steps", type=int, default=10000)
    entropy_cmd.set_defaults(func=cmd_entropy)

    # attractors
    attract_cmd = sub.add_parser("attractors", help="detect repeating cycles")
    attract_cmd.add_argument("--dim", type=int, default=4)
    attract_cmd.add_argument("--steps", type=int, default=10000)
    attract_cmd.set_defaults(func=cmd_attractors)

    # scan
    scan_cmd = sub.add_parser("scan", help="scan entropy across dimensions")
    scan_cmd.add_argument("--dims", nargs=2, type=int, default=[3, 8])
    scan_cmd.add_argument("--steps", type=int, default=10000)
    scan_cmd.set_defaults(func=cmd_scan)

    # symmetry
    sym_cmd = sub.add_parser("symmetry", help="measure symbolic symmetry")
    sym_cmd.add_argument("--dim", type=int, default=4)
    sym_cmd.add_argument("--steps", type=int, default=10000)
    sym_cmd.set_defaults(func=cmd_symmetry)

    # entropy curve experiment
    curve_cmd = sub.add_parser("entropy-curve", help="plot entropy vs dimension")
    curve_cmd.add_argument("--start", type=int, default=3)
    curve_cmd.add_argument("--end", type=int, default=12)
    curve_cmd.add_argument("--steps", type=int, default=20000)
    curve_cmd.set_defaults(func=cmd_entropy_curve)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
