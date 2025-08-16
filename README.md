# Daily Startup Job Digest Bot

This repo automates:
- Fetching **entry-level** roles at top startups (Lever & Greenhouse boards).
- Generating a daily email digest (job title, company, link, short desc).
- Creating a **personalized LinkedIn outreach** blurb for each role.
- Sending email at **12:00 PM IST** and a preview at **10:25 AM IST**.

## Quick Start

### 1) Fork & push this repo
- Put this code in a GitHub repository (public or private).

### 2) Choose mail provider
Recommended: **SendGrid** (easiest). Alternative: Gmail API (advanced).

#### Option A — SendGrid (recommended)
- Create account → add a **Single Sender** (your email `nalindalal2004@gmail.com`) and **verify** it.
- Create API Key with "Full Access".
- In GitHub → **Settings → Secrets and variables → Actions → New repository secret**:
  - `SENDGRID_API_KEY` = your key
  - `MAIL_FROM` = `nalindalal2004@gmail.com`
  - `MAIL_TO` = `nalindalal2004@gmail.com`

#### Option B — Gmail API (OAuth2) (advanced)
- Create a Google Cloud project → enable Gmail API.
- Configure OAuth consent (External) and create **OAuth client credentials**.
- Use a local helper to obtain a **refresh token** for your Gmail account.
- Add these GitHub **secrets**:
  - `GMAIL_CLIENT_ID`
  - `GMAIL_CLIENT_SECRET`
  - `GMAIL_REFRESH_TOKEN`
  - `MAIL_FROM` = `nalindalal2004@gmail.com`
  - `MAIL_TO` = `nalindalal2004@gmail.com`
- In `jobs/email.py`, set `MAIL_PROVIDER="gmail"`.

### 3) (Optional) Edit target companies
- Open `jobs/config.json` → tweak the list of **top startups** and their job boards.
- We use **public JSON endpoints** for Lever & Greenhouse (no login).

### 4) Push and enable GitHub Actions
- Commit & push.
- Go to **Actions** tab → enable workflows if prompted.

### 5) Schedules (IST → UTC)
- Daily digest: **12:00 IST** → `06:30 UTC`
- Preview: **10:25 IST** → `04:55 UTC`

The workflow runs both schedules. You can also trigger manually with **Run workflow**.

---

## How it works

- **Sources**: `LeverSource`, `GreenhouseSource` fetch postings via public JSON.
- **Filter** to _entry-level_: matches keywords like `new grad`, `junior`, `entry`, `graduate`, `I`, `Level 1`.
- **Dedup**: keeps a small JSON database in the workflow cache to avoid emailing stale jobs.
- **Email**: HTML digest + per-role LinkedIn outreach draft.
- **Preview mode**: Shows the first 3 items to sanity-check formatting.

---

## Local run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python jobs/main.py --mode preview
```

Set environment variables if running locally with SendGrid:
```bash
export SENDGRID_API_KEY=...
export MAIL_FROM=nalindalal2004@gmail.com
export MAIL_TO=nalindalal2004@gmail.com
```

---

## File layout

```
jobs/
  main.py
  email.py
  templates.py
  utils.py
  sources/
    lever.py
    greenhouse.py
  config.json
.github/workflows/
  daily-jobs.yml
requirements.txt
```

---

## Notes

- Sites like Wellfound/AngelList or YC Waats often require auth; this bot sticks to **public endpoints** for reliability.
- You can extend `jobs/sources/` with more providers.
- If a company changes their job board provider, update `config.json`.
