# Shorts Auto Editor v7

Windows 기반 YouTube Shorts 자동 생산 GUI 시스템.

## 설치
1. Python 3.10+ 설치
2. `pip install -r requirements.txt`
3. ffmpeg 설치 후 `C:/ffmpeg/bin/ffmpeg.exe` 경로 확인

## 실행
```bash
python main.py
```

## 핵심 파이프라인
- inbox 영상 자동 등록 (`workspace/inbox_videos`)
- 전략 파일(PDF/HTML) 파싱 또는 AI 전략 생성
- 전략 점수화 및 상위 3개 기본 생산
- EDL/SRT/CSV/JSON/preview/burn-in/AI 패키지/업로드 패키지 생성
- 업로드 큐 등록
- 성과 기록 및 추천 엔진 반영

## 출력 구조
`workspace/projects/project_xxx/` 하위에 전략 산출물, analytics, logs, final_manifest 생성.

## 문제 해결
- ffmpeg 오류: `C:/ffmpeg/bin/ffmpeg.exe` 존재 여부 확인.
- burn-in 미생성: SRT 미존재/빈 파일이면 정상 skip(log only).
- 전략 0개: 전략 파일 포맷 점검(헤더 `1 제목`, 세그먼트 `1 [N]` 형태).
