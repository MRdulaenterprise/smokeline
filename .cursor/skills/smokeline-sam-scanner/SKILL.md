---
name: smokeline-sam-scanner
description: Runs the Smokeline SAM.gov opportunity scanner and interprets the output. Use when the user mentions SAM.gov, opportunities, solicitations, "scanner", "opportunity scan", forestry/ROW/vegetation management contracting, or when they need to generate a SAM.gov opportunities report.
---

# Smokeline — SAM.gov Opportunity Scanner

This skill helps you run a Python script that searches the SAM.gov Opportunities API, scores opportunities (high/medium/low fit), and generates a human-readable report plus raw JSON.

## Security (API key)

- **Do not paste API keys in chat.**
- Use an environment variable: `SAM_GOV_API_KEY`

## Quick start

1. Get a SAM.gov public API key (Opportunities API).
2. Set the API key in your shell session:

```bash
export SAM_GOV_API_KEY="YOUR_KEY"
```

3. Install dependency + run:

```bash
pip install requests
python3 ".cursor/skills/smokeline-sam-scanner/smokeline_sam_scanner.py"
```

Outputs are written to the current working directory:
- `smokeline_sam_results.txt`
- `smokeline_sam_results.json`

## What to do with results

- Start with **HIGH FIT** and anything **closing within 14 days**.
- Open each SAM.gov link, download attachments, and confirm:
  - scope and deliverables
  - due date/time zone and submission method
  - required forms and instructions

## Troubleshooting

- **401 Unauthorized**: API key missing/incorrect (`SAM_GOV_API_KEY`).
- **429 Rate limit**: reduce keywords / run less often / consider higher-limit key.
- **requests missing**: `pip install requests` (in the same environment you run Python).

