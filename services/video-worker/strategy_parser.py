from __future__ import annotations
from dataclasses import dataclass, field
import re
from bs4 import BeautifulSoup

SEGMENT_PATTERN = re.compile(r"^\d+\s+\[[NA]\]")
TITLE_PATTERN = re.compile(r"^(10|[1-9])")

@dataclass
class ParsedStrategy:
    strategy_number: int
    strategy_title: str
    segments: list[str] = field(default_factory=list)

def valid_title(line: str) -> bool:
    s = line.strip()
    if len(s) < 5 or not TITLE_PATTERN.match(s):
        return False
    if re.search(r"\[(N|A)\]", s):
        return False
    if SEGMENT_PATTERN.match(s):
        return False
    return True

def parse_html(html: str) -> list[ParsedStrategy]:
    soup = BeautifulSoup(html, "html.parser")
    lines = [x.get_text(" ", strip=True) for x in soup.select("table tr, article *, main *, body *") if x.get_text(strip=True)]
    results: dict[int, ParsedStrategy] = {}
    current = None
    for line in lines:
        if valid_title(line):
            num = int(line.split()[0])
            current = results.setdefault(num, ParsedStrategy(strategy_number=num, strategy_title=line))
            continue
        if current and SEGMENT_PATTERN.match(line):
            current.segments.append(line)
    return [s for _, s in sorted(results.items()) if s.segments]
