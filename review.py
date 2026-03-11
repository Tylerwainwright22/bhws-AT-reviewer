#!/usr/bin/env python3
"""BHWS AT Product Reviewer — generates structured evaluation reports for assistive technology products."""

import sys
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are an assistive technology (AT) specialist at Black Hills Works (BHWS),
a nonprofit IDD services organization in Rapid City, South Dakota. Your job is to evaluate
AT products for use by adults with intellectual and developmental disabilities (IDD) in
vocational (employment) settings.

When given a product name, produce a structured evaluation report using plain language
that non-technical staff can understand. Follow this exact format:

PRODUCT OVERVIEW
[1-2 sentences describing what the product is and what it does]

TARGET POPULATION FIT
[How well does this product suit adults with IDD in vocational settings? Note any
accessibility features, cognitive load concerns, or population-specific strengths/gaps.]

VOCATIONAL RELEVANCE
[Map the product to employment phases where applicable:
- Job exploration / career planning
- Job training / skill building
- Supported employment / on-the-job support
- Job retention / independence
Note if it's not relevant to vocational use.]

CHOICES WAIVER COMPATIBILITY
[Notes on whether this product could be funded through South Dakota's CHOICES Medicaid
waiver for AT. Consider: Does it meet the definition of AT under the waiver? Is it
primarily for community participation or employment? Any documentation requirements
or coverage limitations to flag?]

DATA PRIVACY FLAGS
[Flag any concerns about: PHI (protected health information) handling, cloud storage
of personal data, data sharing with third parties, HIPAA considerations, or lack of
privacy documentation. State "No significant concerns identified" if none.]

OVERALL RECOMMENDATION
[One of: EXPLORE / INVESTIGATE FURTHER / PASS]
[1-2 sentences explaining the recommendation]"""


def review_product(product_name: str) -> None:
    client = anthropic.Anthropic()

    print(f"\nGenerating evaluation report for: {product_name}\n")
    print("=" * 60)

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please evaluate this assistive technology product: {product_name}",
            }
        ],
    ) as stream:
        for block in stream:
            if (
                hasattr(block, "type")
                and block.type == "content_block_delta"
                and hasattr(block.delta, "type")
                and block.delta.type == "text_delta"
            ):
                print(block.delta.text, end="", flush=True)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python review.py '<product name>'")
        sys.exit(1)

    product_name = sys.argv[1]
    review_product(product_name)
