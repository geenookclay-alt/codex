from __future__ import annotations
from pathlib import Path
import argparse
import subprocess
from services.common import logger

INBOX = Path("workspace/inbox_videos")

def duration_seconds(path: Path) -> float:
    # conservative probe: if ffprobe unavailable, return 0 and continue.
    try:
        out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nokey=1:noprint_wrappers=1", str(path)])
        return float(out.decode().strip())
    except Exception:
        return 0.0

def scan_inbox() -> list[dict]:
    INBOX.mkdir(parents=True, exist_ok=True)
    assets = []
    for f in INBOX.glob("*.*"):
        assets.append({"filename": f.name, "rough_title": f.stem.replace("_", " "), "duration": duration_seconds(f), "status": "new"})
    logger.info("detected %s assets", len(assets))
    return assets

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    parser.parse_args()
    print(scan_inbox())
