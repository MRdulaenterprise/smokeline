---
name: hostinger-openclaw-smokeline-sam-scanner
description: "Run the Smokeline Forestry SAM.gov opportunity scanner. Get a SAM.gov API key, configure and run the script, read the report (high/medium/low fit, deadlines), and take next steps for bidding. For Smokeline Forestry (Wilmington, NC) and similar forestry/ROW contractors."
compatibility: "Requires a SAM.gov account and public API key; Python 3 with requests. Can run on Hostinger VPS, local machine, or anywhere with network access."
---

# Smokeline Forestry — SAM.gov Opportunity Scanner

This skill walks you through running the **Smokeline SAM.gov scanner**: a script that searches federal contract opportunities on [SAM.gov](https://sam.gov) for forestry, tree, right-of-way clearing, utility forestry, wildfire management, and related work. Results are scored (high / medium / low fit), sorted by deadline, and written to a human-readable report and raw JSON.

**Use this skill when:** You want to find federal opportunities that match Smokeline Forestry’s services (or similar contractors). You need a SAM.gov API key and a place to run Python (Hostinger VPS, your laptop, or an OpenClaw environment with shell access).

**If you get lost:** Jump back to the step number you last completed and continue from there.

**Security:** Never paste your SAM.gov API key in chat. You will add it only in the script file or environment on the server.

---

## Before you start — Prerequisites

- **SAM.gov account** — Required to request an API key. If you don’t have one, sign up at [sam.gov](https://sam.gov).
- **Python 3** — Installed where you will run the script (Hostinger VPS, Docker container, or local).
- **Network access** — The script calls `https://api.sam.gov/prod/opportunities/v2/search`; firewall must allow outbound HTTPS.
- **Script location** — The scanner script is in this repo: `smokeline_sam_scanner.py`. Run it from the repo root or copy it to a working directory.

---

## Where you are & what we're doing

| Step | What we do |
|------|------------|
| **1** | Get a SAM.gov public API key and note the rate limit (10 requests/day for unregistered key) |
| **2** | Configure the scanner script (API key, date range, keywords) on the server or working directory |
| **3** | Install dependencies and run the scanner |
| **4** | Read and use the reports (high/medium/low fit, urgent deadlines, top picks) |
| **5** | Next steps for bidding (SAM.gov registration, POC contact, NAICS/size standards) |

---

## Step 1 — Get a SAM.gov API key

The scanner uses the **SAM.gov Opportunities API** (v2). You need a **public API key**.

### 1.1 Request the key

1. Log in to [SAM.gov](https://sam.gov).
2. Go to **Entity Management** (or **My SAM**) and find **API Keys** (or **Public API Key** under your profile/account).
3. Request a **public API key** for the Opportunities API. SAM.gov may email the key or show it once; save it somewhere safe (e.g. password manager).
4. **Rate limit:** Unregistered/public keys are typically limited to **10 API requests per day**. The script runs one request per keyword; with 6 default keywords you use 6 of 10. If you hit the limit, the script will stop and report "Rate limit exceeded." For higher limits, check SAM.gov’s **registered API key** options.

**Done when:** You have the API key value (e.g. `SAM-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) saved securely. You will paste it only into the script file on the server — never in chat.

---

## Step 2 — Configure the scanner script

The script is in this repo: `smokeline_sam_scanner.py`. Run it from the repo root or copy it to a directory on your server or laptop. Results will be written in the **current working directory** where you invoke the script.

### 2.1 Set the API key

On the server (or in the copy of the script), open `smokeline_sam_scanner.py` and find the line:

```python
API_KEY = "SAM-01ac97b1-19f8-4188-91b6-c4819cd60c11"  # Your SAM.gov public API key
```

Replace the value with **your** API key. Save the file. Do not commit this file with a real key to a public repo; add it to `.gitignore` if the folder is in version control.

### 2.2 (Optional) Adjust date range and keywords

At the top of the script you can change:

- **`DAYS_BACK`** — How far back to search (default `90` = last 3 months).
- **`KEYWORDS`** — List of search terms. Defaults include: forestry, tree, right of way clearing, utility forestry, wild fire management, trail management.
- **`EXPANDED_SEARCH`** — Set to `True` to also search expanded keywords (vegetation management, timber, brush clearing, prescribed burn, hazard tree, etc.). More keywords = more API calls = easier to hit the 10/day limit.

**Done when:** `API_KEY` in the script is your key, and (optionally) `DAYS_BACK` and `KEYWORDS` are set as you want.

---

## Step 3 — Install dependencies and run the scanner

Run the script where Python 3 and network access are available (e.g. Hostinger VPS, Docker container, or your laptop).

### 3.1 Install requests

```bash
pip install requests
```

If you use a virtual environment or Docker, activate it first, then run the command above.

### 3.2 Run the script

From the directory that contains `smokeline_sam_scanner.py` (e.g. this repo root):

```bash
python3 smokeline_sam_scanner.py
```

The script will:

- Print progress per keyword (and stop with a message if it hits the rate limit or gets 401).
- Write **smokeline_sam_results.txt** — human-readable report (high/medium/low fit, urgent deadlines, top picks, next steps).
- Write **smokeline_sam_results.json** — raw data (scan date, date range, keyword counts, full opportunity list).

If you run from this repo root, the result files appear here. If you copied the script elsewhere, they appear in that working directory.

**Done when:** The script runs without errors (or you see a clear rate-limit/401 message) and you have `smokeline_sam_results.txt` and `smokeline_sam_results.json` in the current directory.

---

## Step 4 — Read and use the reports

### 4.1 Human-readable report (`.txt`)

Open **smokeline_sam_results.txt**. It includes:

- **Date range** and **total unique opportunities** (active, non-expired).
- **Counts by fit:** High fit, Medium fit, Low fit.
- **Closing within 14 days** — urgent list.
- **Results by keyword** — how many hits per search term.
- **Sections by fit:**  
  - **HIGH FIT** — forestry, wildfire, trail, right-of-way, etc.  
  - **MEDIUM FIT** — tree, vegetation, utility clearing, timber.  
  - **LOW FIT** — review manually (may include false positives).
- **TOP PRIORITY PICKS** — top 3 high-fit (or medium-fit if no high).
- **URGENT — CLOSING WITHIN 14 DAYS** — deadlines soon.
- **NEXT STEPS** — short checklist (review links, download attachments, contact POC, SAM.gov registration, NAICS/size, watch for USFS/BLM/FEMA/Army Corps).

Use the report to prioritize which opportunities to open on SAM.gov (use the links in the report).

### 4.2 Raw data (`.json`)

**smokeline_sam_results.json** contains the full opportunity list and metadata (scan_date, date_range, keyword_counts, errors). Use it for automation, filtering, or feeding into other tools. Do not share this file if it might be considered sensitive.

**Done when:** You’ve opened the report, identified high-fit and urgent opportunities, and have the SAM.gov links to review and download solicitations.

---

## Step 5 — Next steps for bidding

The report’s **NEXT STEPS** section summarizes these; reinforce them with the user as needed:

1. **Review high-fit opportunities first** — Open each SAM.gov link from the report; read scope and requirements.
2. **Download solicitation attachments** — Full scope of work and submission instructions are in the attachments on SAM.gov.
3. **Contact the POC early** — Use the contact info in the report (email/phone) for scope or submission questions.
4. **SAM.gov entity registration** — Smokeline (or the bidding entity) must be registered at [SAM.gov Entity Registration](https://sam.gov/content/entity-registration) to submit offers. Confirm or complete registration.
5. **NAICS and size standards** — For forestry-related work, NAICS 115310 (Support Activities for Forestry) often applies; size standard is **$9M** annual receipts. Confirm the solicitation’s NAICS and size standard.
6. **Agencies to watch** — USFS, BLM, FEMA, Army Corps of Engineers often have forestry/ROW/vegetation management opportunities.

**Done when:** The user has a clear next action (e.g. “Register on SAM.gov,” “Contact POC for opportunity X,” “Download attachments for Y”).

---

## Success checklist

- [ ] SAM.gov API key obtained and stored securely (Step 1)
- [ ] Scanner script configured with your API key (and optional date/keywords) on the server or working directory (Step 2)
- [ ] `pip install requests` and `python3 smokeline_sam_scanner.py` run successfully (Step 3)
- [ ] Report and JSON generated; report reviewed for high-fit and urgent opportunities (Step 4)
- [ ] Next steps for bidding (POC contact, SAM.gov registration, NAICS/size) understood (Step 5)

---

## Troubleshooting

| Problem | What to do |
|--------|------------|
| **Rate limit (429)** | SAM.gov allows ~10 requests/day for public key. Use fewer keywords, or run once per day; consider a registered API key for higher limits. |
| **401 Unauthorized** | API key is wrong or expired. Re-copy the key from SAM.gov into the script (no extra spaces); never paste the key in chat. |
| **Connection error** | Server has no outbound HTTPS to api.sam.gov. Check firewall/VPS/network; try from another machine to confirm. |
| **No such file: smokeline_sam_scanner.py** | Run from the directory that contains the script (e.g. this repo root), or use the full path: `python3 /path/to/smokeline/smokeline_sam_scanner.py`. |
| **ModuleNotFoundError: requests** | Run `pip install requests` in the same environment (venv or container) where you run the script. |
| **Results empty or few** | Try increasing `DAYS_BACK` or enabling `EXPANDED_SEARCH` (watch rate limit). Check that keywords match how agencies post (e.g. "right of way" vs "right-of-way"). |

---

## Quick reference

- **Script:** `smokeline_sam_scanner.py` (repo root)
- **Config:** `API_KEY`, `DAYS_BACK`, `KEYWORDS`, `EXPANDED_SEARCH` at top of script
- **Outputs:** `smokeline_sam_results.txt` (report), `smokeline_sam_results.json` (raw)
- **API:** [SAM.gov Opportunities API v2](https://api.sam.gov/prod/opportunities/v2/search) — public key, ~10 req/day
- **Entity registration:** [sam.gov/content/entity-registration](https://sam.gov/content/entity-registration)
- **NAICS 115310:** Support Activities for Forestry — size standard $9M annual receipts
