from __future__ import annotations

from app.core.matcher import infer_media_type
from app.core.project_model import MatchItem, ProjectData


def apply_matches_to_project(project: ProjectData, matches: list[MatchItem]) -> int:
    clips_by_index = {clip.index: clip for clip in project.clips}
    applied_count = 0

    for match in matches:
        if match.status != "success" or match.target_clip_index is None or not match.media_path:
            continue

        clip = clips_by_index.get(match.target_clip_index)
        if clip is None:
            continue

        clip.media_path = match.media_path
        clip.media_type = match.media_type or infer_media_type(match.media_path)
        clip.status = "matched"
        applied_count += 1

    return applied_count
