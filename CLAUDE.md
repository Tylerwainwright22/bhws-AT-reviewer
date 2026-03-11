# BHWS AT Product Reviewer

## What this is
A Python CLI tool that takes an assistive technology product name as input 
and generates a structured evaluation report for Black Hills Works staff.

## Output should always include
- Product overview (1-2 sentences)
- Target population fit (IDD adults, vocational contexts)
- Vocational relevance (map to employment phases where applicable)
- CHOICES waiver compatibility notes (South Dakota Medicaid AT funding)
- Data privacy flags (any PHI handling, cloud storage concerns)
- Overall recommendation (Explore / Investigate Further / Pass)

## Code style
- Python 3.10+
- Use the anthropic Python SDK for API calls
- Keep it simple: single file, CLI input, printed output
- No database, no web framework
- Requirements tracked in requirements.txt

## Project conventions
- Commit after each working milestone
- Plain language in all output -- this may be read by non-technical staff
