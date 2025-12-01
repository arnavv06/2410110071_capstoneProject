"""
main.py

CLI entrypoint for the Multi-Agent Debate Decision Advisor.

Usage:
    python main.py --claim "claim"
"""

import argparse
from graph import run_debate


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Debate Decision Advisor")
    parser.add_argument("--claim", type=str, required=True, help="The claim to evaluate")
    parser.add_argument("--context", type=str, default=None, help="Optional context")

    args = parser.parse_args()

    print("\nRunning Multi-Agent Debate System\n")
    print(f"Claim: {args.claim}\n")

    result = run_debate(claim=args.claim, context=args.context)

    print("\nFINAL VERDICT")
    print(result)


if __name__ == "__main__":
    main()
