from __future__ import annotations

from app.core.project_model import ProjectData


class MotionManager:
    """Placeholder manager for future motion effect assignment logic."""

    def apply_default_motion(self, project: ProjectData, motion_type: str = "none") -> None:
        # TODO: Replace with real motion mapping tied to Vrew capabilities.
        for clip in project.clips:
            clip.motion_type = motion_type
