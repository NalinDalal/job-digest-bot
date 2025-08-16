import requests
from typing import List, Dict
from ..utils import is_entry_level, looks_engineering

class LeverSource:
    BASE = "https://api.lever.co/v0/postings/{slug}?mode=json"

    def fetch_company(self, slug: str, company_name: str) -> List[Dict]:
        url = self.BASE.format(slug=slug)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        jobs = []
        for item in data:
            title = item.get("text") or ""
            desc = (item.get("descriptionPlain") or "")[:600]
            location = None
            if item.get("categories"):
                loc = item["categories"].get("location")
                location = loc
            apply_url = item.get("hostedUrl") or item.get("applyUrl") or item.get("hostedUrl")
            if not apply_url:
                continue
            blob = f"{title}\n{desc}"
            if not looks_engineering(blob):
                continue
            if not is_entry_level(blob):
                continue
            jobs.append({
                "title": title.strip(),
                "company": company_name,
                "url": apply_url,
                "location": location,
                "description": desc
            })
        return jobs
