# Vrew Image Match Auto (MVP Skeleton)

PySide6 desktop skeleton for matching text items to clips and media by number-based indexing.

## Requirements
- Python 3.11+
- PySide6

## Install
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python -m app.main
```

## MVP Workflow
1. Open Project (`.json` or `.txt` mock project)
2. Open Text File (`.txt` with `001|text` or `.srt`)
3. Open Media Folder (`001.png`, `002.jpg`, `005.mp4`, ...)
4. Run Match
5. Apply Matches
6. Save Output (defaults to non-overwriting `*_matched.json`)

## Notes
- Reader/writer are placeholder implementations for quick iteration.
- Real Vrew schema support should be implemented in `app/io/vrew_reader.py` and `app/io/vrew_writer.py`.
