# Shorts Auto Editor v3

Windows용 Python GUI 앱으로, 전략 문서(PDF/HTML)와 원본 영상을 받아 전략별 편집 산출물/AI 패키지를 생성합니다.

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

## 주요 기능
- 전략 파일 입력: PDF(.pdf), HTML(.html/.htm)
- 파서 분기:
  - PDF: `pdfplumber`
  - HTML: `BeautifulSoup`
    - table/tr/td 우선 파싱
    - 실패 시 텍스트 fallback 파싱
- 공통 내부 데이터 모델: `Strategy`, `Segment`
- 전략 헤더/세그먼트 블록 파싱
- 전략별 출력:
  - EDL/SRT/CSV/JSON
  - ffmpeg preview mp4
  - optional burn-in mp4
  - AI 패키지 파일 일괄 생성
- tkinter GUI
- 디버그 로그 강화

## 출력 구조
```text
output/
  strategy_01_제목/
    strategy_01.edl
    strategy_01.srt
    strategy_01.csv
    strategy_01.json
    preview/
      strategy_01_제목.mp4
      strategy_01_제목_subtitled.mp4
    ai/
      strategy_01_hook.txt
      strategy_01_title_candidates.txt
      strategy_01_thumbnail_copy.txt
      strategy_01_metadata.json
      codex_prompt.txt
  manifest.json
```

## 디버그 로그 항목
- `sys.executable`
- `python version`
- `pdfplumber.__file__` (PDF 파싱 시)
- `bs4 import 성공 여부`
- `ffmpeg path`
- `input file type`
- `total lines or extracted text length`
- `detected strategies`
- `segment block counts`
- `generated file paths`
- `errors with stderr`

## 문제해결
1. **ffmpeg 경로 오류**
   - GUI에서 `ffmpeg.exe` 절대 경로 지정
   - 또는 PATH 등록 후 `ffmpeg`만 입력

2. **PDF 텍스트 추출이 빈 경우**
   - 스캔 PDF일 수 있음(OCR 필요)
   - 텍스트 기반 PDF 사용 권장

3. **HTML 테이블 파싱 실패**
   - 자동으로 텍스트 fallback 파싱 수행

4. **Windows 경로 이슈**
   - 파일명 자동 sanitize 처리
   - burn-in 자막 필터에서 백슬래시/콜론 이스케이프 처리
