from __future__ import annotations

from app.core.project_model import Clip


class PreviewService:
    def get_preview_text(self, clip: Clip | None) -> str:
        if clip is None:
            return "No clip selected."

        return (
            f"Clip #{clip.index}\n"
            f"Text: {clip.text}\n"
            f"Status: {clip.status}\n"
            f"Media: {clip.media_path or 'N/A'}"
        )
