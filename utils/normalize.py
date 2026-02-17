import re

TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+"
)

def normalize_line(line: str) -> str:
    return TIMESTAMP_RE.sub("",line)
