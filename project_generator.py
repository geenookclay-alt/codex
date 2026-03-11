from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ai_packager import package_ai
from edl_writer import write_edl
from models import Project, Strategy
from subtitle_builder import build_srt
from upload_packager import build_upload_package
from utils import ensure_dir, save_csv, save_json, safe_title
from video_builder import make_burn_in, make_preview


@dataclass
class GenerateOptions:
    ffmpeg_path: str
    subtitle_style: str = "rhythm"
    make_preview: bool = True
    make_burnin: bool = False
    make_ai: bool = True
    make_upload: bool = True


class ProjectGenerator:
    def __init__(self, logger: Callable[[str], None]) -> None:
        self.logger = logger

    def generate(self, project: Project, strategies: list[Strategy], project_dir: Path, source_video: Path, opts: GenerateOptions) -> Path:
        outputs = ensure_dir(project_dir / "outputs")
        manifest: dict = {"project_id": project.project_id, "items": []}

        for s in strategies[:3]:
            folder = ensure_dir(outputs / f"strategy_{s.strategy_number:02d}_{safe_title(s.strategy_title)}")
            base = folder / f"strategy_{s.strategy_number:02d}"
            edl = write_edl(s, base.with_suffix(".edl"))
            srt = build_srt(s, base.with_suffix(".srt"), opts.subtitle_style)
            rows = [{"segment": seg.get("line", "")} for seg in s.segments] or [{"segment": "auto"}]
            save_csv(base.with_suffix(".csv"), rows)
            save_json(base.with_suffix(".json"), s.to_dict())
            save_json(folder / f"strategy_{s.strategy_number:02d}_evaluation.json", {
                "hook_score": s.hook_score,
                "emotion_score": s.emotion_score,
                "clarity_score": s.clarity_score,
                "shorts_fit_score": s.shorts_fit_score,
                "overall_score": s.overall_score,
            })

            preview_dir = ensure_dir(folder / "preview")
            preview_path = preview_dir / f"strategy_{s.strategy_number:02d}_{safe_title(s.strategy_title)}.mp4"
            burn_path = preview_dir / f"strategy_{s.strategy_number:02d}_{safe_title(s.strategy_title)}_subtitled.mp4"
            if opts.make_preview:
                make_preview(source_video, preview_path, opts.ffmpeg_path, self.logger)
            if opts.make_burnin:
                make_burn_in(source_video, srt, burn_path, opts.ffmpeg_path, self.logger)

            if opts.make_ai:
                package_ai(s, ensure_dir(folder / "ai"))
            if opts.make_upload:
                build_upload_package(s, ensure_dir(folder / "upload"))

            manifest["items"].append({"strategy": s.strategy_number, "path": str(folder), "edl": str(edl), "srt": str(srt)})
            self.logger(f"generated output paths={folder}")

        manifest_path = project_dir / "final_manifest.json"
        save_json(manifest_path, manifest)
        self.logger(f"final manifest path={manifest_path}")
        return manifest_path
