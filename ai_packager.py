from __future__ import annotations

import json
from pathlib import Path

from models import Strategy


class AIPackager:
    def create(self, strategy: Strategy, ai_dir: Path) -> list[Path]:
        ai_dir.mkdir(parents=True, exist_ok=True)
        num = f"{strategy.number:02}"
        files: dict[str, str] = {
            f"strategy_{num}_hook.txt": self._hook(strategy),
            f"strategy_{num}_title_candidates.txt": self._titles(strategy),
            f"strategy_{num}_thumbnail_copy.txt": self._thumb(strategy),
            "codex_prompt.txt": self._prompt(strategy),
        }
        written: list[Path] = []
        for name, content in files.items():
            p = ai_dir / name
            p.write_text(content, encoding="utf-8")
            written.append(p)

        meta_path = ai_dir / f"strategy_{num}_metadata.json"
        meta_path.write_text(json.dumps(strategy.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(meta_path)
        return written

    def _hook(self, s: Strategy) -> str:
        first = s.segments[0].audio_text if s.segments else s.title
        return f"{s.title}\nHook: {first}"

    def _titles(self, s: Strategy) -> str:
        return "\n".join([f"{s.title} | 버전 {i}" for i in range(1, 6)])

    def _thumb(self, s: Strategy) -> str:
        return f"강렬한 표정 + '{s.title}' 텍스트\n대비 높은 컬러 사용"

    def _prompt(self, s: Strategy) -> str:
        return f"전략 {s.number}({s.title}) 기반 쇼츠 메타데이터 생성 프롬프트"
