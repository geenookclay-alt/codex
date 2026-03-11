# Shorts Auto Editor v5

원본 영상(+선택 전략 파일)을 입력하면 **전략 파싱/보강 또는 자동 생성**, 전략 점수화, 편집 결과(EDL/SRT/CSV/JSON/preview/burn-in), AI 패키지, 업로드 패키지를 생성하는 Windows tkinter 앱입니다.

## 요구사항
- Python 3.10+
- Windows
- ffmpeg/ffprobe
- 기본 ffmpeg 경로: `C:/ffmpeg/bin/ffmpeg.exe`

## 설치
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 실행
```bash
python main.py
```

## 모드
- **모드 A (전략 파일 있음)**: PDF/HTML 파싱 → AI 보강(옵션) → 점수화
- **모드 B (전략 파일 없음)**: AI 전략 자동 생성(5/10/20) → 점수화

## 핵심 정책
- `DEFAULT_FFMPEG_PATH = r"C:/ffmpeg/bin/ffmpeg.exe"`
- HTML 파싱 순서: container-first → table parsing → text fallback
- 전략 헤더는 `1~10 + 제목`만 허용, `1 [N]`/`2 [A]` 형태는 제외
- 세그먼트 0개 전략은 제거
- burn-in skip은 오류창이 아니라 로그로만 기록

## 출력 구조
```text
output_root/
  strategies_generated.json
  strategy_rankings.json
  manifest.json
  strategy_01_제목/
    strategy_01.edl
    strategy_01.srt
    strategy_01.csv
    strategy_01.json
    strategy_01_evaluation.json
    ai/
      strategy_01_hook.txt
      strategy_01_title_candidates.txt
      strategy_01_thumbnail_copy.txt
      strategy_01_description.txt
      strategy_01_hashtags.txt
      strategy_01_metadata.json
      codex_prompt.txt
    preview/
      strategy_01_제목.mp4
      strategy_01_제목_subtitled.mp4
    upload/
      final_title.txt
      final_description.txt
      final_hashtags.txt
      final_thumbnail_copy.txt
      upload_checklist.txt
```

## 문제 해결
- ffmpeg 경로 오류: GUI ffmpeg 경로 확인(기본값 자동 입력)
- 전략 파일 헤더 인식 실패: `번호 + 제목` 형식 유지
- burn-in 미생성: SRT 파일 존재/크기 확인(로그에 skip 사유 출력)
