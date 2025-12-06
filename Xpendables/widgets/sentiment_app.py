# widgets/sentiment_app.py
import tkinter as tk, threading, subprocess, sys, os, re, tkinter.messagebox as tkmsg
from tkinter import ttk   # <-- NEW
from neo4j import GraphDatabase
from settings import SCRIPT_DIR, subprocess_env, URI, AUTH
from app_state import state
from widgets.admin_screen import AdminScreen  # -- import our new widget


class SentimentAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Xpendables: Sentiment Analysis")
        self.master.geometry("1100x800")
        self.master.configure(bg="#000000")

        # ----- ttk DARK THEME STYLING (similar to HistoryWindow) -----
        style = ttk.Style(self.master)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TLabel",
            background="#000000",
            foreground="white",
            font=("Arial", 11),
        )
        style.configure(
            "Header.TLabel",
            background="#000000",
            foreground="white",
            font=("Helvetica", 16, "bold"),
        )
        style.configure(
            "TEntry",
            fieldbackground="#1E1E1E",
            foreground="white",
        )
        style.configure(
            "TButton",
            background="#222222",
            foreground="white",
        )
        style.map(
            "TButton",
            background=[("active", "#444444")],
        )

        self.frame = tk.Frame(master, bg="#000000", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # ----- Header -----
        ttk.Label(
            self.frame,
            text="Xpendables: Movie Sentiment Analysis Tool",
            style="Header.TLabel",
        ).pack(pady=10)

        # ----- Keyword row -----
        keyf = tk.Frame(self.frame, bg="#000000")
        keyf.pack(pady=5)

        ttk.Label(
            keyf,
            text="Enter Movie Keyword:",
        ).pack(side=tk.LEFT, padx=5)

        self.keyword_entry = ttk.Entry(
            keyf,
            font=("Arial", 12),
            width=30,
        )
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # ----- Text area (bordered black panel + scrollbar) -----
        textf = tk.Frame(
            self.frame,
            bg="#000000",
            highlightbackground="#444444",
            highlightthickness=1,
            bd=0,
        )
        textf.pack(pady=15, padx=40, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(textf)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 8), pady=8)

        self.output_text = tk.Text(
            textf,
            wrap=tk.WORD,
            font=("Consolas", 11),
            background="#000000",
            foreground="#FFFFFF",
            insertbackground="white",
            relief=tk.FLAT,
            bd=0,
            yscrollcommand=scrollbar.set,
        )
        self.output_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=(8, 0),
            pady=8,
        )
        scrollbar.config(command=self.output_text.yview)

        # tags
        self.output_text.tag_config("dim", foreground="#6b7280")
        self.output_text.tag_config("label", foreground="#9ca3af", font=("Consolas", 11, "bold"))
        self.output_text.tag_config("pos", foreground="#22c55e")
        self.output_text.tag_config("neu", foreground="#60a5fa")
        self.output_text.tag_config("neg", foreground="#f97373")
        self.output_text.tag_config("sep", foreground="#9ca3af")
        self.output_text.tag_config("mono", font=("Consolas", 11))
        self.output_text.tag_config("pad", lmargin1=8, lmargin2=8)
        self.output_text.tag_config("pad2", lmargin1=20, lmargin2=20)
        self.output_text.tag_config("h2", font=("Arial", 13, "bold"))
        self.output_text.tag_config("badge_pos", foreground="#22c55e")
        self.output_text.tag_config("badge_neu", foreground="#60a5fa")
        self.output_text.tag_config("badge_neg", foreground="#f97373")

        self._counts = {"positive": 0, "neutral": 0, "negative": 0}

        # ----- Buttons -----
        btnf = tk.Frame(self.frame, bg="#000000")
        btnf.pack(pady=10)

        ttk.Button(
            btnf,
            text="Fetch Tweets",
            command=self.open_fetch_tweets,
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            btnf,
            text="Analyze Sentiment",
            command=self.open_sentiment_analysis,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            btnf,
            text="Run Full Analysis",
            command=self.run_full_pipeline,
        ).grid(row=1, column=0, columnspan=2, pady=8)

        ttk.Button(
            btnf,
            text="History",
            command=self.open_history_viewer,
        ).grid(row=2, column=0, pady=8)

        ttk.Button(
            btnf,
            text="Admin",
            command=self.open_admin_screen,
        ).grid(row=2, column=1, pady=8)

    # --- helpers identical to your current logic (unchanged) ---
    def _append(self, t, *tags):
        self.output_text.insert(tk.END, t if t.endswith("\n") else t + "\n", tags)
        self.output_text.see(tk.END)

    def _clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self._counts = {"positive": 0, "neutral": 0, "negative": 0}

    def _pretty_ingest_line(self, line: str):
        if not hasattr(self, "_blk"):
            self._blk = {"raw": None, "cleaned": None, "sent": None, "score": None}
        s = line.strip()
        if s.startswith("RAW:"):
            self._blk = {"raw": s[4:].strip(), "cleaned": None, "sent": None, "score": None}
            return
        if s.startswith("CLEANED:"):
            if self._blk.get("raw") is not None:
                self._blk["cleaned"] = s[8:].strip()
                return
        if "SENTIMENT:" in s:
            m_sent = re.search(r"SENTIMENT:\s*([A-Za-z]+)", s)
            m_score = re.search(r"Score:\s*([+-]?\d*\.?\d+)", s)
            self._blk["sent"] = (m_sent.group(1) if m_sent else "Neutral")
            self._blk["score"] = float(m_score.group(1)) if m_score else None
            return
        if set(s) == {"-"}:
            self._emit_block(
                self._blk.get("raw"),
                self._blk.get("cleaned"),
                self._blk.get("sent"),
                self._blk.get("score"),
            )
            fs = (self._blk.get("sent") or "neutral").lower()
            if fs in self._counts:
                self._counts[fs] += 1
            self._blk = {"raw": None, "cleaned": None, "sent": None, "score": None}
            return
        self._append(s, "dim", "pad", "mono")

    def _emit_block(self, raw, cleaned, sent, score):
        if not any([raw, cleaned, sent]):
            return
        s = (sent or "neutral").lower()
        tag = {"positive": "pos", "negative": "neg", "neutral": "neu"}.get(s, "neu")
        self.output_text.insert(tk.END, "● ", (tag, "pad", "mono"))
        self.output_text.insert(tk.END, (sent or "Neutral").title(), (tag, "mono"))
        if score is not None:
            self.output_text.insert(tk.END, f"  (score: {score})", ("dim", "mono"))
        self.output_text.insert(tk.END, "\n", ("mono",))
        if raw is not None:
            self.output_text.insert(tk.END, "RAW: ", ("label", "pad2", "mono"))
            self.output_text.insert(tk.END, raw.strip() + "\n", ("mono",))
        if cleaned is not None:
            self.output_text.insert(tk.END, "CLEANED: ", ("label", "pad2", "mono"))
            self.output_text.insert(tk.END, (cleaned.strip() or "—") + "\n", ("mono",))
        if sent is not None:
            self.output_text.insert(tk.END, "SENTIMENT: ", ("label", "pad2", "mono"))
            self.output_text.insert(
                tk.END,
                sent.title() + (f"  (score: {score})" if score is not None else "") + "\n\n",
                (tag, "mono"),
            )
        self.output_text.insert(tk.END, "═" * 78 + "\n", ("sep", "mono"))
        self.output_text.see(tk.END)

    def append_output(self, out):
        try:
            self._pretty_ingest_line(out)
        except Exception:
            self._append(out)
        print(out)

    # --- pipeline commands (unchanged) ---
    def run_full_pipeline(self):
        threading.Thread(target=self._run_pipeline_thread, daemon=True).start()

    def _run_pipeline_thread(self):
        kw = self.keyword_entry.get().strip()
        if not kw:
            return self.master.after(0, self.append_output, "Please enter a movie keyword first.")
        fetch_path = os.path.join(SCRIPT_DIR, "fetch_tweets.py")
        analyze_path = os.path.join(SCRIPT_DIR, "analyze_sentiment.py")
        raw_path = os.path.join(SCRIPT_DIR, "raw_tweets.txt")
        try:
            self.master.after(0, self._clear_output)
            self.master.after(0, self.append_output, "[Fetch] starting…")
            p = subprocess.Popen(
                [sys.executable, fetch_path, kw, (state.CURRENT_USER or "")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=SCRIPT_DIR,
                env=subprocess_env(),
            )
            for line in p.stdout:
                self.master.after(0, self.append_output, line.strip())
            ferr = p.stderr.read()
            if ferr:
                self.master.after(0, self.append_output, f"Fetch Errors:\n{ferr}")
            code = p.wait()
            self.master.after(0, self.append_output, f"Tweet fetching completed (code: {code})")
            if code != 0 and not os.path.exists(raw_path):
                return self.master.after(
                    0,
                    self.append_output,
                    "No tweets to analyze (fetch failed and no cache).",
                )

            self.master.after(0, self.append_output, "— Analysis —")
            q = subprocess.Popen(
                [sys.executable, analyze_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=SCRIPT_DIR,
                env=subprocess_env(),
            )
            for line in q.stdout:
                self.master.after(0, self.append_output, line.strip())
            qerr = q.stderr.read()
            if qerr:
                self.master.after(0, self.append_output, f"Analysis Errors:\n{qerr}")
            acode = q.wait()
            self.master.after(0, self.append_output, f"Sentiment analysis completed (code: {acode})")
        except Exception as e:
            self.master.after(0, self.append_output, f"Exception occurred: {e}")

    def open_fetch_tweets(self):
        threading.Thread(target=self.run_fetch_tweets).start()

    def run_fetch_tweets(self):
        def _run():
            kw = self.keyword_entry.get().strip()
            if not kw:
                return self.master.after(0, self.append_output, "Please enter a movie keyword first.")
            self.master.after(0, self.append_output, "Fetching tweets for sentiment analysis...")
            script = os.path.join(SCRIPT_DIR, "fetch_tweets.py")
            try:
                p = subprocess.Popen(
                    [sys.executable, script, kw, (state.CURRENT_USER or "")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=SCRIPT_DIR,
                    env=subprocess_env(),
                )
                for line in p.stdout:
                    self.master.after(0, self.append_output, line.strip())
                err = p.stderr.read()
                if err:
                    self.master.after(0, self.append_output, f"Error:\n{err}")
                rc = p.wait()
                self.master.after(
                    0,
                    self.append_output,
                    f"Tweet fetching completed with return code: {rc}",
                )
            except Exception as e:
                self.master.after(0, self.append_output, f"Exception occurred: {e}")

        threading.Thread(target=_run, daemon=True).start()

    def open_sentiment_analysis(self):
        threading.Thread(target=self.run_sentiment_analysis).start()

    def run_sentiment_analysis(self):
        def _run():
            self.master.after(
                0, self.append_output, "Cleaning tweets and preparing for sentiment analysis..."
            )
            script = os.path.join(SCRIPT_DIR, "analyze_sentiment.py")
            try:
                p = subprocess.Popen(
                    [sys.executable, script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=SCRIPT_DIR,
                    env=subprocess_env(),
                )
                for line in p.stdout:
                    self.master.after(0, self.append_output, line.strip())
                err = p.stderr.read()
                if err:
                    self.master.after(0, self.append_output, f"Error:\n{err}")
                rc = p.wait()
                self.master.after(
                    0,
                    self.append_output,
                    f"Sentiment cleaning completed with return code: {rc}",
                )
            except Exception as e:
                self.master.after(0, self.append_output, f"Exception occured: {e}")

        threading.Thread(target=_run, daemon=True).start()

    def open_history_viewer(self):
        from widgets.history_window import HistoryWindow

        wait = tk.Toplevel(self.master)
        wait.title("History")
        wait.geometry("260x80")
        wait.transient(self.master)
        tk.Label(wait, text="Connecting to database…").pack(expand=True, pady=16)

        def _connect():
            try:
                driver = GraphDatabase.driver(URI, auth=AUTH)
                driver.verify_connectivity()
                self.master.after(
                    0, lambda: (wait.destroy(), HistoryWindow(self.master, driver))
                )
            except Exception as e:
                self.master.after(
                    0,
                    lambda: (
                        wait.destroy(),
                        tkmsg.showerror(
                            "Neo4j Connection Error", f"Could not connect:\n{e}"
                        ),
                    ),
                )

        threading.Thread(target=_connect, daemon=True).start()

    def open_admin_screen(self):
        """
        Open the AdminScreen window that shows UNSCORED_WORD frequencies.
        AdminScreen is a Toplevel, so this just pops a new window over the main app.
        """
        AdminScreen(self.master)
