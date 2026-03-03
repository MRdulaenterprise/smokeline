# Smokeline — SAM.gov Opportunity Scanner

Federal contract opportunity scanner for **Smokeline Forestry** (Wilmington, NC) and similar forestry / right-of-way / vegetation management contractors. Searches [SAM.gov](https://sam.gov) for opportunities matching forestry, tree, ROW clearing, utility forestry, wildfire management, trail management, and related keywords.

## What’s in this repo

- **smokeline_sam_scanner.py** — Python script that calls the SAM.gov Opportunities API, scores results (high/medium/low fit), and writes a human-readable report and JSON.
- **SKILL.md** — Step-by-step guide (get API key, configure script, run, read reports, next steps for bidding). For use as an OpenClaw skill or as a standalone walkthrough.
- **skill.yaml** — OpenClaw skill manifest; use with OpenClaw if you install this repo as a skill.

## Quick start

1. **Get a SAM.gov API key** — Log in at [sam.gov](https://sam.gov), request a public API key (Opportunities API). Note: ~10 requests/day for unregistered keys.
2. **Configure** — Edit `smokeline_sam_scanner.py` and set `API_KEY` to your key. Optionally adjust `DAYS_BACK` and `KEYWORDS`.
3. **Run** — `pip install requests` then `python3 smokeline_sam_scanner.py`. Results are written to `smokeline_sam_results.txt` and `smokeline_sam_results.json` in the current directory.

For full instructions (prerequisites, troubleshooting, next steps for bidding), follow **SKILL.md**.

## Repo

- **GitHub:** [MRdulaenterprise/smokeline](https://github.com/MRdulaenterprise/smokeline)

**Proprietary.** MRDula Enterprise, LLC. All rights reserved.
