import requests
from typing import List, Dict
from ..utils import is_entry_level, looks_engineering

class GreenhouseSource:
    BASE = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"

    def fetch_company(self, slug: str, company_name: str) -> List[Dict]:
        url = self.BASE.format(slug=slug)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        jobs = []
        for item in data.get("jobs", []):
            title = item.get("title") or ""
            apply_url = item.get("absolute_url")
            location = None
            if item.get("locations"):
                location = item["locations"][0].get("name")
            elif item.get("location"):
                location = item["location"].get("name")
            # content may contain HTML; cut down for signal
            desc = (item.get("content") or "").replace("<", " ").replace(">", " ")
            desc = " ".join(desc.split())
            desc = desc[:600]

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
