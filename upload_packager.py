from __future__ import annotations

from pathlib import Path

from models import Strategy


class UploadPackager:
    def create(self, strategy: Strategy, upload_dir: Path) -> list[Path]:
        upload_dir.mkdir(parents=True, exist_ok=True)
        files = {
            "final_title.txt": strategy.title,
            "final_description.txt": f"{strategy.title}\n\n핵심 장면 요약 쇼츠 버전입니다.",
            "final_hashtags.txt": "#쇼츠 #shorts #영상편집 #카지노 #전략",
            "final_thumbnail_copy.txt": "반전주의",
            "upload_checklist.txt": "\n".join(
                [
                    "- preview 확인 완료",
                    "- burn-in 확인 완료",
                    "- 제목 선택 필요",
                    "- 설명 선택 필요",
                    "- 해시태그 선택 필요",
                ]
            ),
        }
        written: list[Path] = []
        for name, content in files.items():
            path = upload_dir / name
            path.write_text(content, encoding="utf-8")
            written.append(path)
        return written
