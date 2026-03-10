from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from ai_packager import AIPackager
from edl_writer import EDLWriter
from models import Strategy
from subtitle_builder import SubtitleBuilder
from utils import LogFn, SEGMENT_START_PATTERN, ensure_dir, safe_filename
from video_builder import VideoBuilder


@dataclass
class GenerateOptions:
    subtitle_style: str
    make_preview: bool
    make_burnin: bool
    make_ai: bool
    selected_numbers: list[int] | None = None


class ProjectGenerator:
    def __init__(self, ffmpeg_path: str, log: LogFn):
        self.log = log
        self.sub_builder = SubtitleBuilder()
        self.edl_writer = EDLWriter()
        self.video_builder = VideoBuilder(ffmpeg_path, log)
        self.ai_packager = AIPackager()

    def generate(self, output_dir: Path, input_video: Path, strategies: list[Strategy], options: GenerateOptions) -> Path:
        ensure_dir(output_dir)
        manifest: dict[str, list[str]] = {"generated": []}

        if len(strategies) > 10:
            self.log("경고: 전략 개수가 비정상적으로 많습니다. HTML 헤더 탐지를 재검토하세요.")

        selected = [s for s in strategies if not options.selected_numbers or s.number in options.selected_numbers]
        valid_strategies = [s for s in selected if s.segments]
        self.log(f"final valid strategies={len(valid_strategies)}")

        if not valid_strategies:
            self._log_empty_valid_debug(selected)

        for strategy in valid_strategies:
            folder_name = f"strategy_{strategy.number:02}_{safe_filename(strategy.title)}"
            sdir = ensure_dir(output_dir / folder_name)
            preview_dir = ensure_dir(sdir / "preview")

            edl_path = sdir / f"strategy_{strategy.number:02}.edl"
            srt_path = sdir / f"strategy_{strategy.number:02}.srt"
            csv_path = sdir / f"strategy_{strategy.number:02}.csv"
            json_path = sdir / f"strategy_{strategy.number:02}.json"

            edl_path.write_text(self.edl_writer.build_edl(strategy), encoding="utf-8")
            srt_content = self.sub_builder.build_srt(strategy, options.subtitle_style)
            srt_path.write_text(srt_content, encoding="utf-8")
            self._write_csv(csv_path, strategy)
            json_path.write_text(json.dumps(strategy.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

            generated = [edl_path, srt_path, csv_path, json_path]

            if options.make_preview:
                preview_path = preview_dir / f"strategy_{strategy.number:02}_{safe_filename(strategy.title)}.mp4"
                self.video_builder.build_preview(input_video, preview_path)
                generated.append(preview_path)

            if options.make_burnin:
                burn_path = preview_dir / f"strategy_{strategy.number:02}_{safe_filename(strategy.title)}_subtitled.mp4"
                if not srt_content.strip():
                    self.log(f"burn-in skipped reason=SRT 파일 비어 있음: {srt_path}")
                else:
                    ok, reason = self.video_builder.maybe_burn_in_subtitle(input_video, srt_path, burn_path)
                    if ok:
                        generated.append(burn_path)
                    else:
                        self.log(f"burn-in skipped reason={reason}")

            if options.make_ai:
                ai_dir = ensure_dir(sdir / "ai")
                generated.extend(self.ai_packager.create(strategy, ai_dir))

            for p in generated:
                self.log(f"generated file paths={p}")
                manifest["generated"].append(str(p))

        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        self.log(f"generated file paths={manifest_path}")
        return manifest_path

    def _log_empty_valid_debug(self, strategies: list[Strategy]) -> None:
        titles = [f"{s.number}. {s.title}" for s in strategies]
        self.log(f"detected strategy titles={titles}")

        preview_lines: list[str] = []
        for strategy in strategies:
            preview_lines.append(f"{strategy.number} {strategy.title}")
            for line in strategy.description.splitlines():
                stripped = line.strip()
                if stripped:
                    preview_lines.append(stripped)
        preview_100 = preview_lines[:100]
        self.log(f"first 100 lines preview={preview_100}")

        segment_candidates: list[str] = []
        for line in preview_lines:
            if SEGMENT_START_PATTERN.match(line) or re.match(r"^\d+\s+\[[NA]\]", line):
                segment_candidates.append(line)
        self.log(f"segment start candidates={segment_candidates[:100]}")

    def _write_csv(self, csv_path: Path, strategy: Strategy) -> None:
        with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["idx", "mode", "audio_text", "caption_text", "estimated_seconds", "timecodes", "visual_note"])
            for seg in strategy.segments:
                writer.writerow([seg.idx, seg.mode, seg.audio_text, seg.caption_text, seg.estimated_seconds, "|".join(seg.timecodes), seg.visual_note])
