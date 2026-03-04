# OpenClaw Skills (workspace)

This directory contains OpenClaw skills. Load them by pointing OpenClaw at this repo’s `skills/` folder (workspace skills) or by copying each skill into `~/.openclaw/skills/`.

## Skills

| Skill folder | Description |
|--------------|-------------|
| **openclaw-smokeline-sam-scanner** | Run the SAM.gov opportunity scanner; get reports and next steps for bidding. |
| **openclaw-federal-proposal-writer** | Compliance-first federal proposal drafting (Section L/M, DOCX outlines, templates). |
| **openclaw-smokeline-sales-agent** | Draft-only inbound/outbound email agent for eastern NC forestry/tree services; VAPI call → follow-ups. |

## Using this repo with OpenClaw

1. Clone the repo and open it as your workspace, or add this path to `skills.load.extraDirs` in `~/.openclaw/openclaw.json`.
2. Ensure each skill has a valid `skill.yaml` (name, version, author, description, permissions, entryPoint).
3. Validate: `openclaw skills validate skills/openclaw-smokeline-sam-scanner` (and same for other skill folders).

## Scanner quick start

- Set `SAM_GOV_API_KEY` in your environment.
- From repo root: `pip install -r skills/openclaw-smokeline-sam-scanner/requirements.txt && python3 skills/openclaw-smokeline-sam-scanner/smokeline_sam_scanner.py`
- From the skill folder: `pip install -r requirements.txt && python3 smokeline_sam_scanner.py`
- Outputs: `smokeline_sam_results.txt`, `smokeline_sam_results.json` (in current directory).
