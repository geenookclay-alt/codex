from __future__ import annotations

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from parser_factory import create_parser
from project_generator import GenerateOptions, ProjectGenerator
from strategy_generator import StrategyGenerator
from strategy_ranker import StrategyRanker
from utils import DEFAULT_FFMPEG_PATH, ffmpeg_exists, format_python_debug


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Shorts Auto Editor v5")
        self.geometry("1200x850")

        self.strategy_file = tk.StringVar()
        self.video_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.ffmpeg_path = tk.StringVar(value=DEFAULT_FFMPEG_PATH)
        self.memo_text = tk.StringVar()
        self.user_keywords = tk.StringVar()

        self.auto_generate = tk.BooleanVar(value=True)
        self.strategy_count = tk.IntVar(value=10)
        self.style = tk.StringVar(value="혼합형")
        self.platform = tk.StringVar(value="YouTube Shorts")

        self.subtitle_style = tk.StringVar(value="rhythm")
        self.make_preview = tk.BooleanVar(value=True)
        self.make_burnin = tk.BooleanVar(value=False)
        self.make_ai = tk.BooleanVar(value=True)
        self.make_upload = tk.BooleanVar(value=True)

        self._strategies = []
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

        memo_row = ttk.Frame(root)
        memo_row.pack(fill="x", pady=4)
        ttk.Label(memo_row, text="메모", width=18).pack(side="left")
        ttk.Entry(memo_row, textvariable=self.memo_text).pack(side="left", fill="x", expand=True, padx=6)

        kw_row = ttk.Frame(root)
        kw_row.pack(fill="x", pady=4)
        ttk.Label(kw_row, text="사용자 키워드", width=18).pack(side="left")
        ttk.Entry(kw_row, textvariable=self.user_keywords).pack(side="left", fill="x", expand=True, padx=6)

        ai_frame = ttk.LabelFrame(root, text="AI 전략 생성")
        ai_frame.pack(fill="x", pady=6)
        ttk.Checkbutton(ai_frame, text="전략 자동 생성", variable=self.auto_generate).pack(side="left", padx=6)
        ttk.Label(ai_frame, text="전략 개수").pack(side="left")
        ttk.Combobox(ai_frame, values=[5, 10, 20], textvariable=self.strategy_count, width=6, state="readonly").pack(side="left", padx=6)
        ttk.Label(ai_frame, text="스타일").pack(side="left")
        ttk.Combobox(ai_frame, values=["감정형", "정보형", "참교육형", "반전형", "혼합형"], textvariable=self.style, width=10, state="readonly").pack(side="left", padx=6)
        ttk.Label(ai_frame, text="플랫폼").pack(side="left")
        ttk.Combobox(ai_frame, values=["YouTube Shorts", "Instagram Reels", "TikTok"], textvariable=self.platform, width=16, state="readonly").pack(side="left", padx=6)

        review = ttk.LabelFrame(root, text="전략 검토")
        review.pack(fill="both", expand=True, pady=8)
        cols = ("select", "num", "title", "score", "recommended")
        self.tree = ttk.Treeview(review, columns=cols, show="headings", height=10)
        for col, text, w in [
            ("select", "선택", 60),
            ("num", "번호", 60),
            ("title", "전략 제목", 520),
            ("score", "점수", 80),
            ("recommended", "추천", 80),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)
        self.tree.bind("<Double-1>", self._toggle_selected)

        edit_row = ttk.Frame(review)
        edit_row.pack(fill="x", padx=4, pady=4)
        self.edit_title_var = tk.StringVar()
        ttk.Label(edit_row, text="선택 전략 제목 수정").pack(side="left")
        ttk.Entry(edit_row, textvariable=self.edit_title_var).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(edit_row, text="적용", command=self._apply_title_edit).pack(side="left")
        ttk.Button(edit_row, text="전략 불러오기", command=self.refresh_strategies).pack(side="left", padx=6)

        option = ttk.LabelFrame(root, text="생성 옵션")
        option.pack(fill="x", pady=6)
        ttk.Radiobutton(option, text="리듬 자막", value="rhythm", variable=self.subtitle_style).pack(side="left", padx=6)
        ttk.Radiobutton(option, text="영화 자막", value="movie", variable=self.subtitle_style).pack(side="left", padx=6)
        ttk.Checkbutton(option, text="프리뷰 생성", variable=self.make_preview).pack(side="left", padx=10)
        ttk.Checkbutton(option, text="burn-in 생성", variable=self.make_burnin).pack(side="left", padx=10)
        ttk.Checkbutton(option, text="AI 패키지 생성", variable=self.make_ai).pack(side="left", padx=10)
        ttk.Checkbutton(option, text="업로드 패키지 생성", variable=self.make_upload).pack(side="left", padx=10)

        btns = ttk.Frame(root)
        btns.pack(fill="x", pady=4)
        ttk.Button(btns, text="실행", command=self.start_generate).pack(side="right")
        ttk.Button(btns, text="출력 폴더 열기", command=self.open_output_folder).pack(side="right", padx=8)

        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill="x", pady=4)
        self.log_text = tk.Text(root, height=12)
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

    def refresh_strategies(self) -> None:
        strategy_path = self.strategy_file.get().strip()
        if strategy_path and Path(strategy_path).exists():
            parser = create_parser(strategy_path, self.log)
            base = parser.parse(strategy_path)
        else:
            base = []

        if base:
            if self.auto_generate.get():
                StrategyGenerator(self.log).augment_existing(
                    base,
                    self.style.get(),
                    self.platform.get(),
                    self.user_keywords.get(),
                    self.memo_text.get(),
                )
        elif self.auto_generate.get():
            base = StrategyGenerator(self.log).generate(
                count=self.strategy_count.get(),
                style=self.style.get(),
                platform=self.platform.get(),
                source_hint="",
                user_keywords=self.user_keywords.get(),
                memo_text=self.memo_text.get(),
                start_number=1,
            )

        ranked = StrategyRanker().rank(base)
        self._strategies = ranked
        self._render_tree()

    def _render_tree(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for strategy in self._strategies:
            self.tree.insert(
                "",
                "end",
                iid=str(strategy.number),
                values=("Y", strategy.number, strategy.title, f"{strategy.overall_score:.2f}", "Y" if strategy.recommended else "N"),
            )

    def _toggle_selected(self, _event) -> None:
        item = self.tree.focus()
        if not item:
            return
        values = list(self.tree.item(item, "values"))
        values[0] = "N" if values[0] == "Y" else "Y"
        self.tree.item(item, values=values)
        self.edit_title_var.set(values[2])

    def _apply_title_edit(self) -> None:
        item = self.tree.focus()
        if not item:
            return
        values = list(self.tree.item(item, "values"))
        values[2] = self.edit_title_var.get().strip() or values[2]
        self.tree.item(item, values=values)
        for s in self._strategies:
            if s.number == int(values[1]):
                s.title = values[2]

    def open_output_folder(self) -> None:
        if self.output_dir.get().strip() and Path(self.output_dir.get()).exists():
            os.startfile(self.output_dir.get())

    def start_generate(self) -> None:
        self.progress.start(10)
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        try:
            video_path = Path(self.video_file.get().strip())
            output_raw = self.output_dir.get().strip()
            output_dir = Path(output_raw) if output_raw else Path()
            strategy_file_raw = self.strategy_file.get().strip()
            strategy_path = Path(strategy_file_raw) if strategy_file_raw else Path()
            ffmpeg = self.ffmpeg_path.get().strip() or DEFAULT_FFMPEG_PATH

            if not video_path.exists():
                raise ValueError("원본 영상 미선택")
            if not output_raw:
                raise ValueError("출력 폴더 미선택")
            if not ffmpeg_exists(ffmpeg):
                raise ValueError(f"ffmpeg 실행 실패: {ffmpeg}")
            if not self.auto_generate.get() and (not strategy_file_raw or not strategy_path.exists()):
                raise ValueError("전략 자동 생성도 꺼져 있고 전략 파일도 없음")

            if not self._strategies:
                self.refresh_strategies()
            strategies = list(self._strategies)
            if not strategies:
                raise ValueError("valid strategy 0개")

            selected_numbers = [
                int(self.tree.item(item, "values")[1])
                for item in self.tree.get_children()
                if self.tree.item(item, "values")[0] == "Y"
            ]

            options = GenerateOptions(
                subtitle_style=self.subtitle_style.get(),
                make_preview=self.make_preview.get(),
                make_burnin=self.make_burnin.get(),
                make_ai=self.make_ai.get(),
                make_upload=self.make_upload.get(),
                selected_numbers=selected_numbers,
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
