from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from parser_factory import create_parser
from project_generator import GenerateOptions, ProjectGenerator
from utils import detect_file_type, ffmpeg_exists, format_python_debug


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Shorts Auto Editor v3")
        self.geometry("980x760")

        self.strategy_file = tk.StringVar()
        self.video_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.ffmpeg_path = tk.StringVar(value="ffmpeg")
        self.subtitle_style = tk.StringVar(value="rhythm")
        self.make_preview = tk.BooleanVar(value=True)
        self.make_burnin = tk.BooleanVar(value=False)
        self.make_ai = tk.BooleanVar(value=True)
        self.selection_mode = tk.StringVar(value="all")
        self.selected_nums = tk.StringVar(value="1,2,3")

        self._build_ui()
        self.log(format_python_debug())

    def _build_ui(self) -> None:
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        def row_file(label: str, var: tk.StringVar, is_dir: bool = False) -> None:
            r = ttk.Frame(frm)
            r.pack(fill="x", pady=4)
            ttk.Label(r, text=label, width=18).pack(side="left")
            ttk.Entry(r, textvariable=var).pack(side="left", fill="x", expand=True, padx=6)
            ttk.Button(r, text="찾기", command=lambda: self._browse(var, is_dir)).pack(side="left")

        row_file("전략 파일(PDF/HTML)", self.strategy_file)
        row_file("원본 영상", self.video_file)
        row_file("출력 폴더", self.output_dir, True)
        row_file("ffmpeg 경로", self.ffmpeg_path)

        opt = ttk.LabelFrame(frm, text="옵션")
        opt.pack(fill="x", pady=8)
        ttk.Radiobutton(opt, text="리듬 자막", variable=self.subtitle_style, value="rhythm").pack(side="left", padx=5)
        ttk.Radiobutton(opt, text="영화 자막", variable=self.subtitle_style, value="movie").pack(side="left", padx=5)
        ttk.Checkbutton(opt, text="프리뷰 생성", variable=self.make_preview).pack(side="left", padx=8)
        ttk.Checkbutton(opt, text="burn-in 생성", variable=self.make_burnin).pack(side="left", padx=8)
        ttk.Checkbutton(opt, text="AI 패키지 생성", variable=self.make_ai).pack(side="left", padx=8)

        sel = ttk.LabelFrame(frm, text="전략 생성 범위")
        sel.pack(fill="x", pady=8)
        ttk.Radiobutton(sel, text="전체 생성", variable=self.selection_mode, value="all").pack(side="left", padx=5)
        ttk.Radiobutton(sel, text="선택 생성(예: 1,3,7)", variable=self.selection_mode, value="selected").pack(side="left", padx=5)
        ttk.Entry(sel, textvariable=self.selected_nums, width=24).pack(side="left", padx=6)

        ttk.Button(frm, text="실행", command=self.start_generate).pack(anchor="e", pady=8)

        self.log_text = tk.Text(frm, height=28)
        self.log_text.pack(fill="both", expand=True)

    def _browse(self, var: tk.StringVar, is_dir: bool) -> None:
        val = filedialog.askdirectory() if is_dir else filedialog.askopenfilename()
        if val:
            var.set(val)

    def log(self, msg: str) -> None:
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.update_idletasks()

    def start_generate(self) -> None:
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self) -> None:
        try:
            strategy_path = Path(self.strategy_file.get())
            video_path = Path(self.video_file.get())
            output_dir = Path(self.output_dir.get())
            ffmpeg = self.ffmpeg_path.get().strip()

            if not strategy_path.exists() or not video_path.exists() or not output_dir:
                raise ValueError("입력 파일/폴더를 확인하세요.")

            self.log(f"ffmpeg path={ffmpeg}")
            self.log(f"input file type={detect_file_type(strategy_path)}")
            self.log(f"bs4 import 성공 여부=True")

            if not ffmpeg_exists(ffmpeg):
                raise ValueError(f"ffmpeg 실행 파일을 찾을 수 없습니다: {ffmpeg}")

            parser = create_parser(str(strategy_path), self.log)
            strategies = parser.parse(str(strategy_path))
            if not strategies:
                raise ValueError("전략을 찾지 못했습니다.")

            selected = None
            if self.selection_mode.get() == "selected":
                selected = [int(x.strip()) for x in self.selected_nums.get().split(",") if x.strip()]

            options = GenerateOptions(
                subtitle_style=self.subtitle_style.get(),
                make_preview=self.make_preview.get(),
                make_burnin=self.make_burnin.get(),
                make_ai=self.make_ai.get(),
                selected_numbers=selected,
            )
            generator = ProjectGenerator(ffmpeg, self.log)
            manifest = generator.generate(output_dir, video_path, strategies, options)
            messagebox.showinfo("완료", f"생성 완료:\n{manifest}")
        except Exception as e:  # noqa: BLE001
            self.log(f"errors with stderr={e}")
            messagebox.showerror("오류", str(e))
