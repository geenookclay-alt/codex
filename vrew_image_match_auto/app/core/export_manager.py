from __future__ import annotations

from pathlib import Path


def build_output_path(original_path: Path) -> Path:
    """Create a non-destructive output path by adding a suffix."""
    stem = original_path.stem
    suffix = original_path.suffix or ".json"
    candidate = original_path.with_name(f"{stem}_matched{suffix}")

    counter = 1
    while candidate.exists():
        candidate = original_path.with_name(f"{stem}_matched_{counter}{suffix}")
        counter += 1

    return candidate
