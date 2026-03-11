from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from ai_packager import AIPackager
from edl_writer import EDLWriter
from models import Strategy
from subtitle_builder import SubtitleBuilder
from upload_packager import UploadPackager
from utils import ensure_dir, safe_filename
from video_builder import VideoBuilder


@dataclass
class GenerateOptions:
    subtitle_style: str
    make_preview: bool
    make_burnin: bool
    make_ai: bool
    make_upload: bool
    selected_numbers: list[int] | None = None


class ProjectGenerator:
    def __init__(self, ffmpeg_path: str, log):
        self.log = log
        self.sub_builder = SubtitleBuilder()
        self.edl_writer = EDLWriter()
        self.video_builder = VideoBuilder(ffmpeg_path, log)
        self.ai_packager = AIPackager()
        self.upload_packager = UploadPackager()

    def generate(self, output_dir: Path, input_video: Path, strategies: list[Strategy], options: GenerateOptions) -> Path:
        ensure_dir(output_dir)
        selected = [s for s in strategies if not options.selected_numbers or s.number in options.selected_numbers]

        rankings = [
            {
                "strategy_number": s.number,
                "strategy_title": s.title,
                "overall_score": s.overall_score,
                "recommended": s.recommended,
            }
            for s in sorted(selected, key=lambda item: item.overall_score, reverse=True)
        ]
        rankings_path = output_dir / "strategy_rankings.json"
        rankings_path.write_text(json.dumps(rankings, ensure_ascii=False, indent=2), encoding="utf-8")
        self.log(f"strategy rankings path={rankings_path}")

        generated_root = output_dir / "strategies_generated.json"
        generated_root.write_text(json.dumps([s.to_dict() for s in selected], ensure_ascii=False, indent=2), encoding="utf-8")

        manifest: dict[str, object] = {"generated_output_paths": [], "strategies": {}, "rankings_path": str(rankings_path)}
        for strategy in selected:
            folder = ensure_dir(output_dir / f"strategy_{strategy.number:02}_{safe_filename(strategy.title)}")
            preview_dir = ensure_dir(folder / "preview")
            generated: list[Path] = []

            edl_path = folder / f"strategy_{strategy.number:02}.edl"
            srt_path = folder / f"strategy_{strategy.number:02}.srt"
            csv_path = folder / f"strategy_{strategy.number:02}.csv"
            json_path = folder / f"strategy_{strategy.number:02}.json"
            eval_path = folder / f"strategy_{strategy.number:02}_evaluation.json"

            edl_path.write_text(self.edl_writer.build_edl(strategy), encoding="utf-8")
            srt_path.write_text(self.sub_builder.build_srt(strategy, options.subtitle_style), encoding="utf-8")
            self._write_csv(csv_path, strategy)
            json_path.write_text(json.dumps(strategy.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
            eval_path.write_text(
                json.dumps(
                    {
                        "strategy_number": strategy.number,
                        "hook_score": strategy.hook_score,
                        "emotion_score": strategy.emotion_score,
                        "clarity_score": strategy.clarity_score,
                        "shorts_fit_score": strategy.shorts_fit_score,
                        "overall_score": strategy.overall_score,
                        "recommended": strategy.recommended,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            generated.extend([edl_path, srt_path, csv_path, json_path, eval_path])

            preview_path = preview_dir / f"strategy_{strategy.number:02}_{safe_filename(strategy.title)}.mp4"
            if options.make_preview:
                self.video_builder.build_preview(input_video, strategy, preview_path)
                generated.append(preview_path)

            if options.make_burnin:
                burnin_path = preview_dir / f"strategy_{strategy.number:02}_{safe_filename(strategy.title)}_subtitled.mp4"
                source_video = preview_path if preview_path.exists() else input_video
                ok, reason = self.video_builder.maybe_burn_in_subtitle(source_video, srt_path, burnin_path)
                if ok:
                    generated.append(burnin_path)
                else:
                    self.log(f"burn-in skipped reason={reason}")

            if options.make_ai:
                ai_files = self.ai_packager.create(
                    strategy,
                    folder / "ai",
                    options.subtitle_style,
                    [str(path) for path in generated],
                )
                generated.extend(ai_files)

            if options.make_upload:
                generated.extend(self.upload_packager.create(strategy, folder / "upload"))

            self.log(f"generated output paths={[str(path) for path in generated]}")
            manifest["generated_output_paths"] += [str(path) for path in generated]
            manifest["strategies"][str(strategy.number)] = [str(path) for path in generated]

        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        self.log(f"final manifest path={manifest_path}")
        return manifest_path

    def _write_csv(self, path: Path, strategy: Strategy) -> None:
        with path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.writer(handle)
            writer.writerow(["segment_idx", "mode", "audio_text", "caption_text", "estimated_seconds", "timecodes", "visual_note"])
            for segment in strategy.segments:
                writer.writerow(
                    [
                        segment.idx,
                        segment.mode,
                        segment.audio_text,
                        segment.caption_text,
                        segment.estimated_seconds,
                        "|".join(segment.timecodes),
                        segment.visual_note,
                    ]
                )
