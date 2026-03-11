import argparse
import os
import sys

import anthropic


SYSTEM_PROMPT = """You are an assistive technology (AT) evaluator for Black Hills Works (BHWS), \
a nonprofit organization providing services to adults with intellectual and developmental \
disabilities (IDD) in Rapid City, South Dakota.

Your audience is clinical and vocational staff — not engineers or technical specialists. \
Write in plain, clear language. Avoid jargon. If a technical term is necessary, briefly \
explain it.

Key context:
- IDD = Intellectual and Developmental Disabilities
- AT = Assistive Technology (devices or software that support independence and employment)
- CHOICES waiver = South Dakota Medicaid waiver program that can fund AT for eligible individuals
- Vocational context = supported employment, job training, and career development for adults with IDD
- Employment phases: job exploration, job training, on-the-job support, advancement/independence

Your evaluations must be honest, practical, and useful for staff making funding and \
service decisions."""


USER_PROMPT_TEMPLATE = """Please evaluate the following assistive technology product for \
use at Black Hills Works: {product_name}

Provide your evaluation in exactly these six sections, using the headings as shown:

## Product Overview
1-2 sentences describing what the product is and what it does.

## Target Population Fit
Does this product suit adults with IDD in vocational contexts? Note any cognitive load \
concerns, literacy requirements, or adaptability features.

## Vocational Relevance
Map this product to employment phases where applicable: job exploration, job training, \
on-the-job support, advancement/independence. If it does not fit any phase, say so clearly.

## CHOICES Waiver Compatibility
Note whether this product is likely fundable under the South Dakota CHOICES waiver, what \
documentation might be needed, and any known exclusions. Flag uncertainty if the waiver \
fit is unclear.

## Data Privacy Flags
Note any PHI handling, cloud storage, account requirements, data-sharing practices, or \
other privacy concerns relevant to a nonprofit provider. Flag if the product collects \
sensitive data about end users.

## Overall Recommendation
State one of: Explore / Investigate Further / Pass. Follow the label with 2-4 sentences \
explaining your reasoning."""


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


def build_report(product_name: str) -> str:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(product_name=product_name),
            }
        ],
    )
    return response.content[0].text


def print_report(product_name: str, report_text: str) -> None:
    print("=" * 40)
    print("BHWS AT Product Evaluation")
    print(f"Product: {product_name}")
    print("=" * 40)
    print()
    print(report_text)
    print()
    print("=" * 40)
    print("NOTE: This report is AI-generated. Please review before using it")
    print("in funding requests, clinical decisions, or service planning.")
    print("=" * 40)


def main():
    args = parse_args()
    get_api_key()
    report_text = build_report(args.product_name)
    print_report(args.product_name, report_text)


if __name__ == "__main__":
    main()
