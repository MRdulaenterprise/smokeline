# VAPI intake → outputs (template)

## Input (what you may receive)

### A) Structured fields (example shape)

Use whatever keys are provided. Common keys:

```json
{
  "call_id": "<<<FILL>>>",
  "timestamp": "<<<FILL>>>",
  "caller": {
    "name": "<<<FILL/UNKNOWN>>>",
    "phone": "<<<FILL>>>",
    "email": "<<<FILL/UNKNOWN>>>"
  },
  "job": {
    "address": "<<<FILL>>>",
    "city": "<<<FILL>>>",
    "county": "<<<FILL/UNKNOWN>>>",
    "service_requested": "<<<FILL>>>",
    "urgency": "emergency|soon|flexible|unknown"
  },
  "notes": "<<<FILL>>>"
}
```

### B) Transcript (example)
- The transcript may be partial, messy, or missing.

## Output (always produce)

### 1) Situation summary
- `<<<FILL>>>`

### 2) What we still need (questions)
- `<<<FILL>>>`

### 3) Draft email (primary)

**Subject**: `<<<FILL>>>`

Hi `<<<FILL: name or “there”>>>`,

`<<<FILL: 2–5 short paragraphs, direct/confident, value-first>>>`

To get you an accurate estimate, can you reply with:
- `<<<FILL>>>`

If it’s easier, we can do a quick site visit. What works better:
- `<<<FILL: two time windows options>>>`

Thanks,  
`<<<FILL: signature>>>`

**Notes**:
- Do not quote firm pricing.
- If hazards/power lines: emphasize safety and urgency; recommend keeping clear of area.

### 4) SMS-sized version (optional)
`<<<FILL: <= 320 chars>>>`

### 5) Internal notes (CRM-style)
- **Lead type**: `emergency | estimate | commercial | out-of-scope`
- **Job type**: `<<<FILL>>>`
- **Address**: `<<<FILL>>>`
- **Risks**: `<<<FILL>>>`
- **Next action**: `<<<FILL>>>`

### 6) Escalations (human required)
- Pricing/quote/contract: `<<<YES>>>`
- COI / vendor onboarding: `<<<YES/NO>>>`
- Safety hazard / urgent dispatch decision: `<<<YES/NO>>>`

