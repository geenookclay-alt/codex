from __future__ import annotations

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from parser_factory import create_parser
from project_generator import GenerateOptions, ProjectGenerator
from utils import DEFAULT_FFMPEG_PATH, detect_file_type, ffmpeg_exists, format_python_debug


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Shorts Auto Editor v4")
        self.geometry("1100x800")

        self.strategy_file = tk.StringVar()
        self.video_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.ffmpeg_path = tk.StringVar(value=DEFAULT_FFMPEG_PATH)
        self.subtitle_style = tk.StringVar(value="rhythm")
        self.make_preview = tk.BooleanVar(value=True)
        self.make_burnin = tk.BooleanVar(value=False)
        self.make_ai = tk.BooleanVar(value=True)
        self.make_upload = tk.BooleanVar(value=True)
        self.selection_mode = tk.StringVar(value="all")
        self.selected_nums = tk.StringVar(value="1,3,7")

        self._build_ui()
        for line in format_python_debug():
            self.log(line)

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        self._row_file(root, "전략 파일(PDF/HTML)", self.strategy_file, False)
        self._row_file(root, "원본 영상", self.video_file, False)
        self._row_file(root, "출력 폴더", self.output_dir, True)
        self._row_file(root, "ffmpeg 경로", self.ffmpeg_path, False)

        option = ttk.LabelFrame(root, text="옵션")
        option.pack(fill="x", pady=8)
        ttk.Radiobutton(option, text="리듬 자막", value="rhythm", variable=self.subtitle_style).pack(side="left", padx=6)
        ttk.Radiobutton(option, text="영화 자막", value="movie", variable=self.subtitle_style).pack(side="left", padx=6)
        ttk.Checkbutton(option, text="프리뷰 생성", variable=self.make_preview).pack(side="left", padx=10)
        ttk.Checkbutton(option, text="burn-in 생성", variable=self.make_burnin).pack(side="left", padx=10)
        ttk.Checkbutton(option, text="AI 패키지 생성", variable=self.make_ai).pack(side="left", padx=10)
        ttk.Checkbutton(option, text="업로드 패키지 생성", variable=self.make_upload).pack(side="left", padx=10)

        rng = ttk.LabelFrame(root, text="전략 생성 범위")
        rng.pack(fill="x", pady=8)
        ttk.Radiobutton(rng, text="전체 생성", value="all", variable=self.selection_mode).pack(side="left", padx=6)
        ttk.Radiobutton(rng, text="선택 생성(예: 1,3,7)", value="selected", variable=self.selection_mode).pack(side="left", padx=6)
        ttk.Entry(rng, textvariable=self.selected_nums, width=30).pack(side="left", padx=8)

        btns = ttk.Frame(root)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="실행", command=self.start_generate).pack(side="right")
        ttk.Button(btns, text="출력 폴더 열기", command=self.open_output_folder).pack(side="right", padx=8)

        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill="x", pady=6)

        self.log_text = tk.Text(root, height=28)
        self.log_text.pack(fill="both", expand=True)

    def _row_file(self, parent: ttk.Frame, label: str, var: tk.StringVar, is_dir: bool) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label, width=18).pack(side="left")
        ttk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row, text="찾기", command=lambda: self._browse(var, is_dir)).pack(side="left")

    def _browse(self, var: tk.StringVar, is_dir: bool) -> None:
        picked = filedialog.askdirectory() if is_dir else filedialog.askopenfilename()
        if picked:
            var.set(picked)

    def log(self, text: str) -> None:
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.update_idletasks()

    def open_output_folder(self) -> None:
        if self.output_dir.get().strip() and Path(self.output_dir.get()).exists():
            os.startfile(self.output_dir.get())

    def start_generate(self) -> None:
        self.progress.start(10)
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        try:
            strategy_path = Path(self.strategy_file.get().strip())
            video_path = Path(self.video_file.get().strip())
            output_raw = self.output_dir.get().strip()
            output_dir = Path(output_raw) if output_raw else Path()
            ffmpeg = self.ffmpeg_path.get().strip() or DEFAULT_FFMPEG_PATH

            if not strategy_path.exists():
                raise ValueError("전략 파일 미선택")
            if not video_path.exists():
                raise ValueError("원본 영상 미선택")
            if not output_raw:
                raise ValueError("출력 폴더 미선택")
            output_dir.mkdir(parents=True, exist_ok=True)

            self.log(f"input file type={detect_file_type(strategy_path)}")
            if not ffmpeg_exists(ffmpeg):
                raise RuntimeError(f"ffmpeg 실행 자체 실패: {ffmpeg}")

            parser = create_parser(str(strategy_path), self.log)
            strategies = parser.parse(str(strategy_path))
            if not strategies:
                raise ValueError("valid strategy 0개")

            selected = None
            if self.selection_mode.get() == "selected":
                selected = [int(token.strip()) for token in self.selected_nums.get().split(",") if token.strip()]

            options = GenerateOptions(
                subtitle_style=self.subtitle_style.get(),
                make_preview=self.make_preview.get(),
                make_burnin=self.make_burnin.get(),
                make_ai=self.make_ai.get(),
                make_upload=self.make_upload.get(),
                selected_numbers=selected,
            )
            manifest = ProjectGenerator(ffmpeg, self.log).generate(output_dir, video_path, strategies, options)
            messagebox.showinfo("완료", f"생성 완료\n{manifest}")
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            self.log(msg)
            if "burn-in skipped" not in msg:
                messagebox.showerror("오류", msg)
        finally:
            self.progress.stop()
