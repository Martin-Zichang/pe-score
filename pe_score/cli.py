"""
PE-Score 命令行工具
"""

import argparse
import json
import sys
from .scorer import PEScorer
from .dimensions import DIMENSIONS, DIM_NAMES


def main():
    parser = argparse.ArgumentParser(
        prog="pe-score",
        description="PE-Score: Data-driven PE investment scoring framework",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # score 命令
    score_parser = subparsers.add_parser("score", help="Score a project")
    score_parser.add_argument("--name", required=True, help="Project name")
    score_parser.add_argument("--stage", required=True,
                              choices=["seed", "early", "late", "pre_ipo"],
                              help="Investment stage")
    score_parser.add_argument("--scores", type=str,
                              help="35 sub-indicator scores as comma-separated list")
    score_parser.add_argument("--dims", type=str,
                              help="7 dimension scores as comma-separated list (simplified mode)")
    score_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # list 命令
    list_parser = subparsers.add_parser("list", help="List dimensions and sub-indicators")

    # weights 命令
    weights_parser = subparsers.add_parser("weights", help="Show weight schemes")
    weights_parser.add_argument("--stage", choices=["seed", "early", "late", "pre_ipo"],
                                help="Show weights for specific stage")

    args = parser.parse_args()

    if args.command == "score":
        _cmd_score(args)
    elif args.command == "list":
        _cmd_list()
    elif args.command == "weights":
        _cmd_weights(args)
    else:
        parser.print_help()


def _cmd_score(args):
    scorer = PEScorer()

    if args.scores:
        scores = [float(x.strip()) for x in args.scores.split(",")]
        result = scorer.score(args.name, args.stage, scores)
    elif args.dims:
        dim_vals = [float(x.strip()) for x in args.dims.split(",")]
        if len(dim_vals) != 7:
            print("Error: --dims requires exactly 7 values (one per dimension)")
            sys.exit(1)
        dim_dict = dict(zip(DIM_NAMES, dim_vals))
        result = scorer.score_from_dict(args.name, args.stage, dim_dict)
    else:
        print("Error: provide either --scores (35 values) or --dims (7 values)")
        sys.exit(1)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.summary())


def _cmd_list():
    print("PE-Score: 7 Dimensions × 5 Sub-indicators = 35 Indicators\n")
    for i, (dim, subs) in enumerate(DIMENSIONS.items(), 1):
        print(f"{i}. {dim}")
        for j, sub in enumerate(subs, 1):
            print(f"   {i}.{j} {sub}")
        print()


def _cmd_weights(args):
    from .weights import STAGE_WEIGHTS, DEFAULT_WEIGHTS

    if args.stage:
        w = STAGE_WEIGHTS.get(args.stage, DEFAULT_WEIGHTS)
        print(f"\nStage: {args.stage}")
        print("-" * 40)
        for dim, weight in zip(DIM_NAMES, w):
            print(f"  {dim:>4}: {weight*100:5.1f}%")
        print(f"  {'合计':>4}: {sum(w)*100:5.1f}%")
    else:
        print("\nPE-Score Weight Schemes")
        print("=" * 60)
        header = f"{'维度':>4}"
        for stage in STAGE_WEIGHTS:
            header += f"  {stage:>8}"
        print(header)
        print("-" * 60)
        for i, dim in enumerate(DIM_NAMES):
            row = f"{dim:>4}"
            for stage in STAGE_WEIGHTS:
                row += f"  {STAGE_WEIGHTS[stage][i]*100:>7.1f}%"
            print(row)


if __name__ == "__main__":
    main()
