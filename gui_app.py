from __future__ import annotations

import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from analytics_manager import AnalyticsManager
from asset_library import AssetLibrary
from inbox_watcher import InboxWatcher
from models import PerformanceRecord, Project
from parser_factory import create_parser
from project_generator import GenerateOptions, ProjectGenerator
from project_manager import ProjectManager
from queue_manager import QueueManager
from recommendation_engine import RecommendationEngine
from scheduler import next_slot
from settings import DEFAULT_FFMPEG_PATH, DEFAULT_WINDOW_SIZE, DEFAULT_WINDOW_TITLE, INBOX_DIR, PROJECTS_DIR
from strategy_generator import StrategyGenerator
from strategy_ranker import StrategyRanker
from utils import ensure_dir, ffmpeg_exists, format_python_debug, save_json


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(DEFAULT_WINDOW_TITLE)
        self.geometry(DEFAULT_WINDOW_SIZE)

        self.ffmpeg_path = tk.StringVar(value=DEFAULT_FFMPEG_PATH)
        self.video_file = tk.StringVar()
        self.strategy_file = tk.StringVar()
        self.channel_name = tk.StringVar(value="default_channel")
        self.series_name = tk.StringVar(value="default_series")
        self.memo = tk.StringVar()
        self.keywords = tk.StringVar()
        self.auto_generate = tk.BooleanVar(value=True)

        self.make_burn = tk.BooleanVar(value=False)
        self.make_preview = tk.BooleanVar(value=True)
        self.subtitle_style = tk.StringVar(value="rhythm")

        self.strategies = []
        self.project_manager = ProjectManager()
        self.queue_manager = QueueManager()
        self.library = AssetLibrary(self.ffmpeg_path.get())

        self._build_ui()
        for line in format_python_debug(self.ffmpeg_path.get()):
            self.log(line)

        try:
            ensure_dir(INBOX_DIR)
            self.watcher = InboxWatcher(INBOX_DIR, self.library, self.log, poll_sec=8)
            self.watcher.start()
        except Exception as e:
            messagebox.showerror("오류", f"inbox watcher 초기화 실패: {e}")

    def _build_ui(self) -> None:
        top = ttk.Frame(self, padding=8)
        top.pack(fill="both", expand=True)
        tabs = ttk.Notebook(top)
        tabs.pack(fill="both", expand=True)

        self.tab_dashboard = ttk.Frame(tabs)
        self.tab_inbox = ttk.Frame(tabs)
        self.tab_project = ttk.Frame(tabs)
        self.tab_ai = ttk.Frame(tabs)
        self.tab_review = ttk.Frame(tabs)
        self.tab_prod = ttk.Frame(tabs)
        self.tab_queue = ttk.Frame(tabs)
        self.tab_perf = ttk.Frame(tabs)
        self.tab_rec = ttk.Frame(tabs)
        self.tab_log = ttk.Frame(tabs)
        for name, tab in [
            ("대시보드", self.tab_dashboard), ("소재 인박스", self.tab_inbox), ("프로젝트", self.tab_project), ("AI 기획", self.tab_ai),
            ("전략 검토", self.tab_review), ("제작", self.tab_prod), ("업로드 큐", self.tab_queue), ("성과", self.tab_perf),
            ("추천 엔진", self.tab_rec), ("로그/디버그", self.tab_log),
        ]:
            tabs.add(tab, text=name)

        self._build_project_tab()
        self._build_review_tab()
        self._build_queue_tab()
        self._build_perf_tab()
        self.log_text = tk.Text(self.tab_log, height=30)
        self.log_text.pack(fill="both", expand=True)

    def _build_project_tab(self) -> None:
        frame = self.tab_project
        def row(label, var, is_dir=False):
            r = ttk.Frame(frame)
            r.pack(fill="x", pady=3)
            ttk.Label(r, text=label, width=18).pack(side="left")
            ttk.Entry(r, textvariable=var).pack(side="left", fill="x", expand=True)
            if label in ("원본 영상", "전략 파일"):
                ttk.Button(r, text="찾기", command=lambda: var.set(filedialog.askopenfilename())).pack(side="left", padx=4)
            elif label == "ffmpeg":
                ttk.Button(r, text="찾기", command=lambda: var.set(filedialog.askopenfilename())).pack(side="left", padx=4)
        row("원본 영상", self.video_file)
        row("전략 파일", self.strategy_file)
        row("ffmpeg", self.ffmpeg_path)
        row("채널", self.channel_name)
        row("시리즈", self.series_name)
        row("메모", self.memo)
        row("키워드", self.keywords)
        ttk.Checkbutton(frame, text="전략 자동 생성", variable=self.auto_generate).pack(anchor="w")
        ttk.Checkbutton(frame, text="preview 생성", variable=self.make_preview).pack(anchor="w")
        ttk.Checkbutton(frame, text="burn-in 생성", variable=self.make_burn).pack(anchor="w")
        ttk.Button(frame, text="실행", command=self.run_pipeline).pack(anchor="e", pady=8)

    def _build_review_tab(self) -> None:
        self.tree = ttk.Treeview(self.tab_review, columns=("n", "title", "score", "rec"), show="headings")
        for c, t in [("n", "번호"), ("title", "제목"), ("score", "점수"), ("rec", "추천")]:
            self.tree.heading(c, text=t)
        self.tree.pack(fill="both", expand=True)

    def _build_queue_tab(self) -> None:
        self.queue_text = tk.Text(self.tab_queue, height=20)
        self.queue_text.pack(fill="both", expand=True)

    def _build_perf_tab(self) -> None:
        ttk.Button(self.tab_perf, text="추천 갱신", command=self.refresh_recommendation).pack(anchor="e")
        self.rec_text = tk.Text(self.tab_rec, height=20)
        self.rec_text.pack(fill="both", expand=True)

    def log(self, msg: str) -> None:
        if hasattr(self, "log_text"):
            self.log_text.insert("end", msg + "\n")
            self.log_text.see("end")
        self.update_idletasks()

    def run_pipeline(self) -> None:
        video = Path(self.video_file.get().strip())
        if not video.exists():
            messagebox.showerror("오류", "원본 영상 미선택")
            return
        if not ffmpeg_exists(self.ffmpeg_path.get().strip() or DEFAULT_FFMPEG_PATH):
            messagebox.showerror("오류", "ffmpeg 실행 실패")
            return

        parser_input = self.strategy_file.get().strip()
        if not parser_input and not self.auto_generate.get():
            messagebox.showerror("오류", "전략 자동 생성도 꺼져 있고 전략 파일도 없음")
            return

        strategies = []
        if parser_input:
            parser = create_parser(parser_input, self.log)
            strategies = parser.parse(Path(parser_input))
        if not strategies and self.auto_generate.get():
            strategies = StrategyGenerator(self.log).generate(10, "YouTube Shorts", self.keywords.get(), self.memo.get())
        elif strategies:
            strategies = StrategyGenerator(self.log).augment_existing(strategies)
        if not strategies:
            messagebox.showerror("오류", "valid strategy 0개")
            return

        project_id = f"project_{len(list(PROJECTS_DIR.glob('project_*'))) + 1:03d}"
        project = Project(
            project_id=project_id,
            channel_name=self.channel_name.get(),
            series_name=self.series_name.get(),
            project_title=video.stem,
            platform="YouTube Shorts",
            language="ko",
            status="draft",
            source_video_path=str(video),
            strategy_file_path=parser_input,
        )
        pdir = self.project_manager.create_project(project)
        ranked = StrategyRanker().rank(strategies, pdir / "strategy_rankings.json")
        save_json(pdir / "strategies_generated.json", [s.to_dict() for s in ranked])
        self.log(f"strategy rankings path={pdir / 'strategy_rankings.json'}")

        opts = GenerateOptions(
            ffmpeg_path=self.ffmpeg_path.get().strip() or DEFAULT_FFMPEG_PATH,
            subtitle_style=self.subtitle_style.get(),
            make_preview=self.make_preview.get(),
            make_burnin=self.make_burn.get(),
            make_ai=True,
            make_upload=True,
        )
        ProjectGenerator(self.log).generate(project, ranked, pdir, video, opts)

        slot = next_slot(["09:00", "13:00", "20:00"])
        for s in ranked[:3]:
            self.queue_manager.enqueue(project.project_id, s.strategy_number, slot)
        self.log(f"queue update path={self.queue_manager.queue_path}")

        am = AnalyticsManager(pdir / "analytics" / "performance.json")
        for s in ranked[:3]:
            am.append(PerformanceRecord(project.project_id, s.strategy_number, str(date.today()), 0, 0, 0, "", "", "", "init"))
        self.log(f"analytics save path={pdir / 'analytics' / 'performance.json'}")

        self.render_strategy_tree(ranked)
        self.refresh_queue()

    def render_strategy_tree(self, strategies) -> None:
        self.tree.delete(*self.tree.get_children())
        for s in strategies:
            self.tree.insert("", "end", values=(s.strategy_number, s.strategy_title, s.overall_score, "Y" if s.recommended else "N"))

    def refresh_queue(self) -> None:
        self.queue_text.delete("1.0", "end")
        for it in self.queue_manager.list_items():
            self.queue_text.insert("end", f"{it.queue_id} | {it.project_id} | {it.strategy_number} | {it.upload_status} | {it.scheduled_time}\n")

    def refresh_recommendation(self) -> None:
        records = []
        for p in PROJECTS_DIR.glob("project_*/analytics/performance.json"):
            records += AnalyticsManager(p).list_records()
        rec = RecommendationEngine().recommend(records)
        self.rec_text.delete("1.0", "end")
        self.rec_text.insert("end", str(rec))
