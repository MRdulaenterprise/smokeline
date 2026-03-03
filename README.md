# Smokeline — Cursor Skills Pack (SAM.gov + GovCon)

This repo is organized as a **multi-skill** pack for Cursor, focused on:

- Finding opportunities on **SAM.gov**
- Writing **U.S. federal proposals** (compliance-first, Section L/M traceability, DOCX-ready outlines)

## How to use (Cursor)

- **Use in this repo**: open this repository in Cursor. Project skills live under `.cursor/skills/`.
- **Use in another repo**: copy `.cursor/skills/` into the other repository (same path).

## Repo structure

Skills are stored as:

- `.cursor/skills/<skill-name>/SKILL.md`

## Skills included

- **`smokeline-sam-scanner`** (`.cursor/skills/smokeline-sam-scanner/`)
  - Scans SAM.gov Opportunities API for matches and generates `smokeline_sam_results.txt` + `smokeline_sam_results.json`.
  - Includes the runnable script and a step-by-step skill guide.

- **`federal-proposal-writer`** (`.cursor/skills/federal-proposal-writer/`)
  - Compliance-first proposal drafting workflow (Section L/M), compliance matrix, and **DOCX-ready outlines**.

## Example prompts (Cursor chat)

- “Run the `smokeline-sam-scanner` and summarize the top 5 opportunities.”
- “Use `federal-proposal-writer` to build a compliance matrix from Section L/M.”

## Quick start: SAM.gov scanner

1. **Set API key (recommended via env var)**:

```bash
export SAM_GOV_API_KEY="YOUR_KEY"
```

2. **Install dependency + run**:

```bash
pip install requests
python3 ".cursor/skills/smokeline-sam-scanner/smokeline_sam_scanner.py"
```

Outputs are written to your current directory:
- `smokeline_sam_results.txt`
- `smokeline_sam_results.json`

## Notes

- **Security**: do not commit API keys. Use environment variables (or a local `.env` ignored by git).

## Adding a new skill

1. Create a new folder under `.cursor/skills/<new-skill-name>/`
2. Add `SKILL.md` with YAML frontmatter (`name`, `description`)
3. Keep the main `SKILL.md` concise; put longer templates in a sibling markdown file.

