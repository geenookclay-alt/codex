# Shorts Auto Editor v4

전략 파일(PDF/HTML) + 원본 영상 파일을 입력하면 전략별 편집 산출물(EDL/SRT/CSV/JSON), 프리뷰 영상, AI 패키지, 업로드 준비 패키지까지 생성하는 Windows용 tkinter 앱입니다.

## 요구사항
- Python 3.10+
- Windows
- ffmpeg/ffprobe 설치
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

## GUI 입력
1. 전략 파일 (`.pdf`, `.html`, `.htm`)
2. 원본 영상 파일
3. 출력 폴더
4. ffmpeg 경로 (기본값 자동 입력)

## 주요 동작
- 파서 분기
  - PDF: `pdfplumber`
  - HTML: container-first → table parsing → text fallback
- 전략 헤더 검증
  - `^\d{1,2}\s+.+`
  - `^\d{1,2}\s+\[[NA]\]` 제외
  - 번호 1~10 제한
  - 제목 길이 5자 이상
- 세그먼트 파싱
  - `^\d+\s+\[[NA]\]`
  - 추출 필드: idx/mode/audio_text/caption_text/estimated_seconds/timecodes/visual_note
- 자막 스타일
  - rhythm, movie
- 프리뷰 영상
  - 세그먼트 시작 타임코드 기준 part 추출 후 concat
- burn-in
  - SRT 없거나 0바이트면 자동 skip + 로그
- AI 패키지
  - hook/title/thumbnail/description/hashtags/metadata/codex_prompt 생성
- 업로드 패키지
  - final_title/final_description/final_hashtags/final_thumbnail_copy/upload_checklist 생성

## 출력 구조
```text
output_root/
  strategy_01_제목/
    strategy_01.edl
    strategy_01.srt
    strategy_01.csv
    strategy_01.json
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
  manifest.json
```

## 오류 정책
오류창 표시:
- 전략 파일 미선택
- 원본 영상 미선택
- 출력 폴더 미선택
- valid strategy 0개
- ffmpeg 실행 실패

로그만 표시:
- burn-in skip
- 일부 strategy 산출물 skip

## 트러블슈팅
- ffmpeg 경로 문제: GUI의 ffmpeg 입력값 확인 (`C:/ffmpeg/bin/ffmpeg.exe` 권장)
- PDF 텍스트 추출 실패: OCR 없는 스캔 PDF일 수 있음
- HTML 오인식: 전략 헤더에 번호+제목 형식을 유지
