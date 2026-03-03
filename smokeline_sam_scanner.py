#!/usr/bin/env python3
"""
SAM.gov Opportunity Scanner — Smokeline Forestry (Wilmington, NC)
Scans federal contract opportunities matching forestry/tree/ROW services.

Usage:
    pip install requests
    python smokeline_sam_scanner.py

Results are saved to: smokeline_sam_results.txt (human-readable report)
                  and: smokeline_sam_results.json (raw data)
"""

import requests
import json
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  CONFIGURATION — Edit as needed
# ─────────────────────────────────────────────

API_KEY = "SAM-01ac97b1-19f8-4188-91b6-c4819cd60c11"  # Your SAM.gov public API key

DAYS_BACK = 90  # How far back to search (90 = last 3 months)

KEYWORDS = [
    "forestry",
    "tree",
    "right of way clearing",
    "utility forestry",
    "wild fire management",
    "trail management",
]

# Optional: also search these expanded keywords (set EXPANDED_SEARCH = True to enable)
EXPANDED_SEARCH = False
EXPANDED_KEYWORDS = [
    "vegetation management",
    "timber",
    "brush clearing",
    "prescribed burn",
    "hazard tree",
    "forest management",
    "arborist",
    "tree trimming",
    "invasive species",
]

BASE_URL = "https://api.sam.gov/prod/opportunities/v2/search"

# ─────────────────────────────────────────────
#  SCAN LOGIC
# ─────────────────────────────────────────────

def run_scan():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=DAYS_BACK)

    date_from = start_date.strftime("%m/%d/%Y")
    date_to = end_date.strftime("%m/%d/%Y")

    keywords_to_run = KEYWORDS + (EXPANDED_KEYWORDS if EXPANDED_SEARCH else [])

    print("=" * 60)
    print("  SMOKELINE FORESTRY — SAM.gov Opportunity Scanner")
    print("=" * 60)
    print(f"  Date range : {date_from} → {date_to}")
    print(f"  Keywords   : {len(keywords_to_run)}")
    print(f"  Scan time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_results = {}
    keyword_counts = {}
    errors = {}

    for kw in keywords_to_run:
        params = {
            "api_key": API_KEY,
            "keyword": kw,
            "limit": 25,
            "active": "Yes",
            "postedFrom": date_from,
            "postedTo": date_to,
        }
        try:
            resp = requests.get(BASE_URL, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                opps = data.get("opportunitiesData", [])
                keyword_counts[kw] = len(opps)
                print(f"  ✓  '{kw}' → {len(opps)} results")
                for opp in opps:
                    nid = opp.get("noticeId")
                    if nid and nid not in all_results:
                        all_results[nid] = opp
                        all_results[nid]["_matched_keywords"] = [kw]
                    elif nid:
                        all_results[nid]["_matched_keywords"].append(kw)
            elif resp.status_code == 429:
                print(f"  ✗  '{kw}' → RATE LIMIT HIT (10/day max). Stopping.")
                errors[kw] = "Rate limit exceeded"
                break
            elif resp.status_code == 401:
                print(f"  ✗  '{kw}' → UNAUTHORIZED. Check your API key.")
                errors[kw] = "Unauthorized"
                break
            else:
                msg = f"HTTP {resp.status_code}"
                print(f"  ✗  '{kw}' → {msg}")
                errors[kw] = msg
        except requests.exceptions.ConnectionError:
            print(f"  ✗  '{kw}' → Connection error. Check internet connection.")
            errors[kw] = "Connection error"
        except Exception as e:
            print(f"  ✗  '{kw}' → {e}")
            errors[kw] = str(e)

    print(f"\n  Total unique opportunities: {len(all_results)}")
    print()

    return all_results, keyword_counts, errors, date_from, date_to


# ─────────────────────────────────────────────
#  RELEVANCE SCORING
# ─────────────────────────────────────────────

HIGH_FIT_KEYWORDS = ["forestry", "wildfire", "wild fire", "trail", "right of way", "right-of-way"]
MEDIUM_FIT_KEYWORDS = ["tree", "vegetation", "utility clearing", "timber"]
LOW_FIT_KEYWORDS = ["landscaping", "land clearing", "grounds"]

IT_NOISE_TERMS = ["software", "IT", "cyber", "data", "network", "cloud", "system", "tree diagram"]

def score_opportunity(opp):
    title = (opp.get("title") or "").lower()
    keywords = [k.lower() for k in opp.get("_matched_keywords", [])]

    # Deprioritize obvious IT/non-forestry false positives
    for noise in IT_NOISE_TERMS:
        if noise.lower() in title:
            return "low"

    for kw in HIGH_FIT_KEYWORDS:
        if kw in title or kw in " ".join(keywords):
            return "high"
    for kw in MEDIUM_FIT_KEYWORDS:
        if kw in title or kw in " ".join(keywords):
            return "medium"
    return "low"


# ─────────────────────────────────────────────
#  REPORT GENERATION
# ─────────────────────────────────────────────

def format_deadline(dl):
    if not dl:
        return "Not specified"
    try:
        dt = datetime.fromisoformat(dl.replace("Z", ""))
        days_left = (dt - datetime.now()).days
        flag = ""
        if days_left < 0:
            flag = " [EXPIRED]"
        elif days_left <= 7:
            flag = f" ⚠️  CLOSING IN {days_left}d"
        elif days_left <= 14:
            flag = f" ⚡ {days_left}d left"
        return dt.strftime("%Y-%m-%d") + flag
    except:
        return dl[:10] if len(dl) >= 10 else dl


def get_contact(opp):
    contacts = opp.get("pointOfContact") or []
    if contacts:
        c = contacts[0]
        parts = []
        if c.get("email"):
            parts.append(c["email"])
        if c.get("phone"):
            parts.append(c["phone"])
        return " | ".join(parts) if parts else "Not listed"
    return "Not listed"


def generate_report(all_results, keyword_counts, errors, date_from, date_to):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now()

    # Score and sort
    scored = []
    for opp in all_results.values():
        score = score_opportunity(opp)
        opp["_relevance"] = score
        scored.append(opp)

    # Filter: skip expired deadlines for main report
    active_opps = []
    for opp in scored:
        dl = opp.get("responseDeadLine")
        if dl:
            try:
                dt = datetime.fromisoformat(dl.replace("Z", ""))
                if dt < today:
                    continue
            except:
                pass
        active_opps.append(opp)

    # Sort: high fit first, then by deadline
    priority_order = {"high": 0, "medium": 1, "low": 2}
    active_opps.sort(key=lambda x: (
        priority_order.get(x.get("_relevance", "low"), 2),
        x.get("responseDeadLine") or "9999"
    ))

    high = [o for o in active_opps if o["_relevance"] == "high"]
    medium = [o for o in active_opps if o["_relevance"] == "medium"]
    low = [o for o in active_opps if o["_relevance"] == "low"]
    urgent = [o for o in active_opps if o.get("responseDeadLine") and
              (datetime.fromisoformat(o["responseDeadLine"].replace("Z", "")) - today).days <= 14
              if _safe_days(o.get("responseDeadLine")) is not None]

    lines = []
    lines.append("=" * 70)
    lines.append("  SMOKELINE FORESTRY — SAM.gov Scan Report")
    lines.append(f"  Generated: {now}")
    lines.append(f"  Date Range: {date_from} → {date_to}")
    lines.append("=" * 70)
    lines.append(f"\n  Total opportunities found (active, unique): {len(active_opps)}")
    lines.append(f"  High fit: {len(high)}  |  Medium fit: {len(medium)}  |  Low fit: {len(low)}")
    lines.append(f"  Closing within 14 days: {len(urgent)}")

    if errors:
        lines.append(f"\n  ⚠️  Keyword errors: {', '.join(errors.keys())}")

    # Keyword summary
    lines.append("\n" + "-" * 70)
    lines.append("  RESULTS BY KEYWORD")
    lines.append("-" * 70)
    for kw, count in keyword_counts.items():
        lines.append(f"  {kw:<30} {count} results")

    def opp_block(opp, i):
        title = opp.get("title") or "Untitled"
        notice_id = opp.get("noticeId", "")
        sol_num = opp.get("solicitationNumber") or "N/A"
        dept = opp.get("fullParentPathName") or opp.get("department") or "Unknown Agency"
        opp_type = opp.get("type") or "Unknown"
        posted = (opp.get("postedDate") or "")[:10]
        deadline = format_deadline(opp.get("responseDeadLine"))
        naics = opp.get("naicsCode") or "N/A"
        contact = get_contact(opp)
        link = opp.get("uiLink") or f"https://sam.gov/opp/{notice_id}/view"
        matched = ", ".join(opp.get("_matched_keywords", []))

        block = [
            f"\n  [{i}] {title}",
            f"      Agency   : {dept}",
            f"      Type     : {opp_type}",
            f"      Posted   : {posted}  |  Deadline: {deadline}",
            f"      NAICS    : {naics}  |  Matched: {matched}",
            f"      Sol #    : {sol_num}",
            f"      Contact  : {contact}",
            f"      Link     : {link}",
        ]
        return "\n".join(block)

    if high:
        lines.append("\n" + "=" * 70)
        lines.append("  🟢 HIGH FIT OPPORTUNITIES")
        lines.append("=" * 70)
        for i, opp in enumerate(high, 1):
            lines.append(opp_block(opp, i))

    if medium:
        lines.append("\n" + "=" * 70)
        lines.append("  🟡 MEDIUM FIT OPPORTUNITIES")
        lines.append("=" * 70)
        for i, opp in enumerate(medium, 1):
            lines.append(opp_block(opp, i))

    if low:
        lines.append("\n" + "=" * 70)
        lines.append("  ⚪ LOW FIT / REVIEW MANUALLY")
        lines.append("=" * 70)
        for i, opp in enumerate(low, 1):
            lines.append(opp_block(opp, i))

    # Top picks
    top_picks = high[:3] if high else medium[:3]
    if top_picks:
        lines.append("\n" + "=" * 70)
        lines.append("  ⭐ TOP PRIORITY PICKS FOR SMOKELINE FORESTRY")
        lines.append("=" * 70)
        for i, opp in enumerate(top_picks, 1):
            title = opp.get("title") or "Untitled"
            link = opp.get("uiLink") or f"https://sam.gov/opp/{opp.get('noticeId','')}/view"
            deadline = format_deadline(opp.get("responseDeadLine"))
            lines.append(f"\n  {i}. {title}")
            lines.append(f"     Deadline: {deadline}")
            lines.append(f"     Link: {link}")

    if urgent:
        lines.append("\n" + "=" * 70)
        lines.append("  🔴 URGENT — CLOSING WITHIN 14 DAYS")
        lines.append("=" * 70)
        for opp in urgent:
            title = opp.get("title") or "Untitled"
            deadline = format_deadline(opp.get("responseDeadLine"))
            link = opp.get("uiLink") or f"https://sam.gov/opp/{opp.get('noticeId','')}/view"
            lines.append(f"\n  • {title}")
            lines.append(f"    Deadline: {deadline}")
            lines.append(f"    Link: {link}")

    lines.append("\n" + "=" * 70)
    lines.append("  NEXT STEPS")
    lines.append("=" * 70)
    lines.append("  1. Review high-fit opportunities first — open each SAM.gov link")
    lines.append("  2. Download solicitation attachments for full scope of work")
    lines.append("  3. Contact the POC early with any scope questions")
    lines.append("  4. Confirm Smokeline is registered on SAM.gov as a vendor")
    lines.append("     (required to bid): https://sam.gov/content/entity-registration")
    lines.append("  5. Check size standard for NAICS 115310: $9M annual receipts")
    lines.append("  6. Watch for USFS, BLM, FEMA, and Army Corps of Engineers awards")
    lines.append("=" * 70)
    lines.append("\n  Raw data saved to: smokeline_sam_results.json")
    lines.append("=" * 70)

    return "\n".join(lines)


def _safe_days(dl):
    if not dl:
        return None
    try:
        dt = datetime.fromisoformat(dl.replace("Z", ""))
        return (dt - datetime.now()).days
    except:
        return None


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    all_results, keyword_counts, errors, date_from, date_to = run_scan()

    report = generate_report(all_results, keyword_counts, errors, date_from, date_to)

    # Save human-readable report
    report_file = "smokeline_sam_results.txt"
    with open(report_file, "w") as f:
        f.write(report)

    # Save raw JSON
    json_file = "smokeline_sam_results.json"
    with open(json_file, "w") as f:
        json.dump({
            "scan_date": datetime.now().isoformat(),
            "date_range": {"from": date_from, "to": date_to},
            "total_unique": len(all_results),
            "keyword_counts": keyword_counts,
            "errors": errors,
            "opportunities": list(all_results.values()),
        }, f, indent=2)

    print(report)
    print(f"\n  ✅ Report saved to: {report_file}")
    print(f"  ✅ Raw data saved to: {json_file}")
