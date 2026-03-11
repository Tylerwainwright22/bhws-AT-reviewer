import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a structured AT product evaluation report for BHWS staff."
    )
    parser.add_argument(
        "product_name",
        help="Name of the assistive technology product to evaluate.",
    )
    return parser.parse_args()


def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY is not set. Export it before running.")
        sys.exit(1)
    return key


def main():
    args = parse_args()
    get_api_key()
    print(f"Product to evaluate: {args.product_name}")


if __name__ == "__main__":
    main()
