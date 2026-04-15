from __future__ import annotations

from pathlib import Path

from app.core.project_model import MatchItem, ProjectData

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}


def infer_media_type(path: str | None) -> str | None:
    if not path:
        return None
    ext = Path(path).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return "unknown"


def run_number_based_match(
    project: ProjectData,
    text_items: list[dict],
    media_map: dict[int, Path],
) -> list[MatchItem]:
    clips_by_index = {clip.index: clip for clip in project.clips}
    results: list[MatchItem] = []

    for item in text_items:
        source_index = item.get("source_index")
        source_text = item.get("source_text", "")

        if not isinstance(source_index, int):
            results.append(
                MatchItem(
                    source_index=-1,
                    source_text=source_text,
                    target_clip_index=None,
                    media_path=None,
                    media_type=None,
                    match_mode="number",
                    score=0.0,
                    status="invalid_item",
                    error_message="source_index is missing or not an int",
                )
            )
            continue

        clip = clips_by_index.get(source_index)
        media_path = media_map.get(source_index)

        if clip is None:
            results.append(
                MatchItem(
                    source_index=source_index,
                    source_text=source_text,
                    target_clip_index=None,
                    media_path=str(media_path) if media_path else None,
                    media_type=infer_media_type(str(media_path)) if media_path else None,
                    match_mode="number",
                    score=0.0,
                    status="clip_not_found",
                    error_message="No clip with this index",
                )
            )
            continue

        if media_path is None:
            results.append(
                MatchItem(
                    source_index=source_index,
                    source_text=source_text,
                    target_clip_index=clip.index,
                    media_path=None,
                    media_type=None,
                    match_mode="number",
                    score=0.0,
                    status="media_not_found",
                    error_message="No media file with this index",
                )
            )
            continue

        media_path_str = str(media_path)
        results.append(
            MatchItem(
                source_index=source_index,
                source_text=source_text,
                target_clip_index=clip.index,
                media_path=media_path_str,
                media_type=infer_media_type(media_path_str),
                match_mode="number",
                score=1.0,
                status="success",
                error_message=None,
            )
        )

    return results
