from __future__ import annotations

import re
from pathlib import Path


class TextParser:
    def parse(self, path: Path) -> list[dict]:
        ext = path.suffix.lower()
        if ext == ".txt":
            return self._parse_txt(path)
        if ext == ".srt":
            return self._parse_srt(path)
        raise ValueError(f"Unsupported text file type: {ext}")

    def _parse_txt(self, path: Path) -> list[dict]:
        items: list[dict] = []
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split("|", maxsplit=1)
            if len(parts) == 2 and parts[0].strip().isdigit():
                items.append(
                    {
                        "source_index": int(parts[0].strip()),
                        "source_text": parts[1].strip(),
                    }
                )
            else:
                items.append({"source_index": None, "source_text": line})

        return items

    def _parse_srt(self, path: Path) -> list[dict]:
        content = path.read_text(encoding="utf-8")
        blocks = re.split(r"\n\s*\n", content.strip())
        items: list[dict] = []

        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if len(lines) < 3:
                continue

            if not lines[0].isdigit():
                continue

            source_index = int(lines[0])
            # line[1] is the timestamp row
            source_text = " ".join(lines[2:])
            items.append({"source_index": source_index, "source_text": source_text})

        return items
