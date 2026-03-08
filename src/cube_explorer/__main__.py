import argparse
from cube_explorer.hypercube import Hypercube
from cube_explorer.analysis import entropy
from cube_explorer.attractors import find_symbol_cycles


def cmd_run(dim, steps):

    cube = Hypercube(dim)
    seq = cube.random_walk(steps)

    print("\nSymbolic sequence:\n")
    print(" ".join(seq))


def cmd_entropy(dim, steps):

    cube = Hypercube(dim)
    seq = cube.random_walk(steps)

    H = entropy(seq)

    print(f"\nHypercube Q{dim}")
    print(f"Sequence length: {steps}")
    print(f"Entropy: {H:.4f}\n")


def cmd_attractors(dim, steps):

    cube = Hypercube(dim)
    seq = cube.random_walk(steps)

    cycles = find_symbol_cycles(seq)

    print(f"\nHypercube Q{dim}")
    print("\nTop attractor cycles:\n")

    for c in cycles[:10]:
        print(f"{c['cycle']} (len={c['length']}, count={c['occurrences']})")

def cmd_scan(start, end, steps):

    from cube_explorer.analysis import entropy

    print("\nEntropy scan across hypercube dimensions\n")

    for d in range(start, end + 1):

        cube = Hypercube(d)

        seq = cube.random_walk(steps)

        H = entropy(seq)

        print(f"Q{d}: entropy={H:.4f}")

def main():

    parser = argparse.ArgumentParser(
        description="Symbolic Cube Explorer"
    )

    sub = parser.add_subparsers(dest="command")

    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--dim", type=int, default=4)
    run_cmd.add_argument("--steps", type=int, default=50)

    ent_cmd = sub.add_parser("entropy")
    ent_cmd.add_argument("--dim", type=int, default=4)
    ent_cmd.add_argument("--steps", type=int, default=10000)

    att_cmd = sub.add_parser("attractors")
    att_cmd.add_argument("--dim", type=int, default=4)
    att_cmd.add_argument("--steps", type=int, default=10000)

scan_cmd = sub.add_parser("scan")
scan_cmd.add_argument("--dims", nargs=2, type=int, default=[3,8])
scan_cmd.add_argument("--steps", type=int, default=10000)

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(args.dim, args.steps)

    elif args.command == "entropy":
        cmd_entropy(args.dim, args.steps)

    elif args.command == "attractors":
        cmd_attractors(args.dim, args.steps)

    else:
        parser.print_help()

elif args.command == "scan":
    start, end = args.dims
    cmd_scan(start, end, args.steps)

if __name__ == "__main__":
    main()
