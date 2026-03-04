# Smokeline — OpenClaw Skills Pack (SAM.gov + GovCon + Sales)

This repo is an **OpenClaw skill pack** with three skills:

- **SAM.gov opportunity scanning** (forestry/ROW contracting)
- **Federal proposal writing** (Section L/M, DOCX outlines)
- **Forestry/tree sales agent** (draft-only email + VAPI call follow-ups, eastern NC)

## Repo structure

Skills live in the **`skills/`** directory (OpenClaw workspace layout):

```
skills/
├── README.md
├── openclaw-smokeline-sam-scanner/    # SAM.gov scanner script + SKILL.md
├── openclaw-federal-proposal-writer/ # Proposal workflow + templates
└── openclaw-smokeline-sales-agent/   # Email drafts + VAPI playbooks
```

Each skill has a **`skill.yaml`** manifest (name, version, author, description, permissions, entryPoint, triggers).

## How to use with OpenClaw

1. **Workspace**: Use this repo as your OpenClaw workspace so `skills/` is loaded as workspace skills.
2. **Or copy**: Copy any `skills/openclaw-*/` folder into `~/.openclaw/skills/`.
3. **Or extra dir**: Add this repo’s path to `skills.load.extraDirs` in `~/.openclaw/openclaw.json`.

Validate a skill:

```bash
openclaw skills validate skills/openclaw-smokeline-sam-scanner
```

## Skills included

| Skill | Description |
|-------|-------------|
| **openclaw-smokeline-sam-scanner** | Run the SAM.gov Opportunities API scanner; get high/medium/low fit reports and next steps. Requires `SAM_GOV_API_KEY`. |
| **openclaw-federal-proposal-writer** | Compliance-first federal proposal drafting: opportunity summary, compliance matrix, DOCX-ready outlines, templates. |
| **openclaw-smokeline-sales-agent** | Draft-only inbound/outbound emails for eastern NC forestry/tree services; turns VAPI call data into follow-ups and internal notes. |

## Quick start: SAM.gov scanner

1. Set your API key: `export SAM_GOV_API_KEY="YOUR_KEY"`
2. From repo root:

```bash
pip install -r skills/openclaw-smokeline-sam-scanner/requirements.txt
python3 skills/openclaw-smokeline-sam-scanner/smokeline_sam_scanner.py
```

Outputs (in current directory): `smokeline_sam_results.txt`, `smokeline_sam_results.json`

## Adding a new skill

1. Create `skills/openclaw-<new-skill-name>/` (e.g. `skills/openclaw-my-skill/`) with:
   - **skill.yaml** — OpenClaw manifest (name, version, author, description, permissions, entryPoint, optional triggers)
   - **SKILL.md** — Instructions the agent follows (natural-language entry point)
   - Any scripts or templates
2. Validate: `openclaw skills validate skills/openclaw-<new-skill-name>`

## Security

Do not commit API keys. Use environment variables or OpenClaw’s config/vault for secrets.
