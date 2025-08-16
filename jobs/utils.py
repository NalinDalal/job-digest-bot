import re
from dateutil import parser

ENTRY_LEVEL_RE = re.compile(r"""
(\bnew\s*grad(uate)?\b|\bjunior\b|\bentry(-|\s*)level\b|\bgraduate\b|\bengineer\s*I\b|\bSWE\s*I\b|\bL1\b|\bLevel\s*1\b)
""", re.IGNORECASE)

FUNCTION_HINTS_RE = re.compile(r"""
(software|engineer|developer|backend|frontend|full[-\s]*stack|devops|sre|infrastructure|platform|data|ml|ai)
""", re.IGNORECASE)

def is_entry_level(text: str) -> bool:
    if not text:
        return False
    return bool(ENTRY_LEVEL_RE.search(text))

def looks_engineering(text: str) -> bool:
    if not text:
        return False
    return bool(FUNCTION_HINTS_RE.search(text))

def parse_date_safe(s):
    try:
        return parser.parse(s)
    except Exception:
        return None
