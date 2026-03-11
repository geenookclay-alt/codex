from __future__ import annotations

import json
from pathlib import Path

from models import Strategy


class AIPackager:
    def create(self, strategy: Strategy, ai_dir: Path, subtitle_style: str, output_files: list[str]) -> list[Path]:
        ai_dir.mkdir(parents=True, exist_ok=True)
        num = f"{strategy.number:02}"

        hook_candidates = self._hooks(strategy)
        title_candidates = self._title_candidates(strategy)
        thumb_candidates = self._thumbnail_copy(strategy)
        desc_candidates = self._descriptions(strategy)
        hashtags = self._hashtags()

        files = {
            f"strategy_{num}_hook.txt": "\n".join(hook_candidates),
            f"strategy_{num}_title_candidates.txt": "\n".join(title_candidates),
            f"strategy_{num}_thumbnail_copy.txt": "\n".join(thumb_candidates),
            f"strategy_{num}_description.txt": "\n\n".join(desc_candidates),
            f"strategy_{num}_hashtags.txt": "\n".join(hashtags),
            "codex_prompt.txt": self._codex_prompt(strategy),
        }
        written: list[Path] = []
        for name, content in files.items():
            path = ai_dir / name
            path.write_text(content, encoding="utf-8")
            written.append(path)

        metadata = {
            "strategy_number": strategy.number,
            "strategy_title": strategy.title,
            "recommended_title": title_candidates[0],
            "title_candidates": title_candidates,
            "hook_candidates": hook_candidates,
            "thumbnail_copy_candidates": thumb_candidates,
            "description_candidates": desc_candidates,
            "hashtags": hashtags,
            "subtitle_style": subtitle_style,
            "estimated_runtime": round(sum(seg.estimated_seconds for seg in strategy.segments), 2),
            "output_files": output_files,
        }
        mpath = ai_dir / f"strategy_{num}_metadata.json"
        mpath.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(mpath)
        return written

    def _hooks(self, strategy: Strategy) -> list[str]:
        seed = strategy.segments[0].audio_text if strategy.segments else strategy.title
        return [
            f"[rhythm] {seed[:30]}... 지금부터 시작입니다",
            f"[rhythm] 3초 안에 판이 뒤집힙니다: {strategy.title[:25]}",
            f"[rhythm] 이 장면 하나로 결말이 달라집니다",
            f"[movie] {strategy.title}의 핵심, 단 3초에 압축합니다.",
            f"[movie] 방금 본 한 컷이 모든 복선이었습니다.",
        ]

    def _title_candidates(self, strategy: Strategy) -> list[str]:
        base = strategy.title
        return [
            f"(감정형) {base} 보고 멘탈 나간 이유",
            f"(감정형) 이 장면에서 소름 돋은 사람?",
            f"(카운트다운형) {base} 핵심 3포인트",
            f"(카운트다운형) 10초만에 이해하는 {base}",
            f"(참교육형) 오만한 주인공의 최후",
            f"(참교육형) 결국 판을 읽은 사람은 따로 있었다",
            f"(정보형) 쇼츠 편집 포인트로 보는 {base}",
            f"(정보형) 초보도 따라하는 {base} 구성",
            f"(감정형) 결말 알면 다시 보게 되는 스토리",
            f"(카운트다운형) 이 영상에서 꼭 봐야 할 장면 TOP3",
        ]

    def _thumbnail_copy(self, _strategy: Strategy) -> list[str]:
        return ["실화냐", "반전", "충격", "개꿀잼", "미쳤다", "지금봤어?", "결말주의", "판뒤집힘", "이게맞아?", "끝까지봐"]

    def _descriptions(self, strategy: Strategy) -> list[str]:
        return [
            f"{strategy.title} 핵심 장면만 리듬감 있게 압축했습니다. 마지막 반전까지 확인하세요.",
            f"전략 {strategy.number} 기준으로 편집한 쇼츠 버전입니다. 핵심 타임코드와 자막 포인트를 함께 담았습니다.",
            "짧지만 강한 흐름으로 재구성했습니다. 어떤 제목이 가장 끌리는지 댓글로 골라주세요!",
        ]

    def _hashtags(self) -> list[str]:
        return [
            "#쇼츠", "#shorts", "#영상편집", "#영화", "#드라마", "#카지노", "#스토리", "#전략", "#편집", "#viral",
            "#추천", "#반전", "#hook", "#자막", "#premiere", "#ffmpeg", "#ai", "#콘텐츠", "#유튜브", "#shortvideo",
        ]

    def _codex_prompt(self, strategy: Strategy) -> str:
        return (
            f"전략 {strategy.number} '{strategy.title}' 전용 후처리 프롬프트\n"
            "1) 이 전략을 더 자극적으로 재작성\n"
            "2) 제목만 더 공격적으로 20개 생성\n"
            "3) 썸네일 문구를 3~5자/6~10자로 구분해 재생성"
        )
