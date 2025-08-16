import os, json, argparse, datetime
from typing import List, Dict

from .sources.lever import LeverSource
from .sources.greenhouse import GreenhouseSource
from .email import send_email, build_email_bodies

DB_DIR = ".job_db"
DB_FILE = os.path.join(DB_DIR, "seen.json")

def load_config() -> Dict:
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        return json.load(f)

def ensure_db():
    os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"seen": []}, f)

def load_seen() -> set:
    ensure_db()
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return set(data.get("seen", []))

def save_seen(ids: set):
    with open(DB_FILE, "w") as f:
        json.dump({"seen": sorted(list(ids))}, f)

def job_id(j: Dict) -> str:
    return f"{j['company']}::{j['title']}::{j['url']}"

def generate_outreach(role: Dict, user_name="Nalin") -> str:
    company = role['company']
    title = role['title']
    lines = [
        f"Hi {{Name}}, I’m {user_name} — a final-year engineer focused on pragmatic web systems (TypeScript, Go, Rust) and OSS (p5.js). ",
        f"I’m excited about {company}’s work and this {title} role. I’ve been building production-style projects (DevOps-friendly, tests, CI) and I’m comfortable with React/Node/Go, Postgres/Redis, Docker/K8s, and AWS.",
        "If it helps, I can share concise repos and a 1–2 minute loom explaining my recent work. Would you be open to a quick chat or pointing me to the best next step? Thanks!"
    ]
    return "\n".join(lines)

def fetch_all(config: Dict) -> List[Dict]:
    out = []
    le = LeverSource()
    gh = GreenhouseSource()
    for c in config['companies']:
        try:
            if c['provider'] == 'lever':
                jobs = le.fetch_company(c['slug'], c['name'])
            elif c['provider'] == 'greenhouse':
                jobs = gh.fetch_company(c['slug'], c['name'])
            else:
                continue
            for j in jobs:
                j['outreach'] = generate_outreach(j)
            out.extend(jobs)
        except Exception as e:
            # Keep going even if one company fails
            print(f"WARN: {c['name']} failed: {e}")
    # simple sort: company then title
    out.sort(key=lambda x: (x['company'].lower(), x['title'].lower()))
    return out

def filter_new(jobs: List[Dict], seen: set) -> List[Dict]:
    fresh = []
    for j in jobs:
        jid = job_id(j)
        if jid not in seen:
            fresh.append(j)
    return fresh

def trim_for_preview(jobs: List[Dict], max_items: int) -> List[Dict]:
    return jobs[:max_items]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['preview','daily'], default='preview')
    args = ap.parse_args()

    config = load_config()
    jobs = fetch_all(config)

    # Always include all jobs in the email
    email_jobs = jobs
    if args.mode == 'preview':
        email_jobs = trim_for_preview(jobs, config.get('max_items_preview', 5))

    if not email_jobs:
        print("No jobs found; sending digest with 0 roles.")

    # Optionally still update seen for daily mode
    if args.mode == 'daily':
        seen = load_seen()
        new_ids = seen.union({job_id(j) for j in jobs})
        save_seen(new_ids)

    # email
    today = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)  # IST-ish timestamp
    date_str = today.strftime('%d %b %Y, %I:%M %p IST')
    subject = f"Startup Job Digest — {date_str} ({args.mode})"
    text, html = build_email_bodies(email_jobs, date_str, args.mode)
    send_email(subject, text, html)

if __name__ == '__main__':
    main()

