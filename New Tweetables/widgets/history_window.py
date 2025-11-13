# widgets/history_window.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from neo4j import GraphDatabase

class HistoryWindow(tk.Toplevel):
    def __init__(self, master, driver):
        super().__init__(master)
        self.title("Tweetables — History")
        self.geometry("1100x1000")
        self.configure(bg="#F3F4F6")

        self.limit = 100
        self.skip  = 0
        self.driver = driver  # already opened by caller

        # Filters
        filt = tk.Frame(self, bg="#F3F4F6"); filt.pack(side=tk.TOP, fill=tk.X, padx=12, pady=8)
        def L(r,c,t): tk.Label(filt, text=t, bg="#F3F4F6").grid(row=r, column=c, sticky="w")

        L(0,0,"Keyword:");      self.keyword_var = tk.StringVar(); ttk.Entry(filt, textvariable=self.keyword_var, width=18).grid(row=0, column=1, padx=6)
        L(0,2,"Run ID:");       self.run_var = tk.StringVar(); self.run_combo = ttk.Combobox(filt, textvariable=self.run_var, width=40); self.run_combo.grid(row=0, column=3, padx=6)
        L(0,4,"Username:");     self.user_var = tk.StringVar(); ttk.Entry(filt, textvariable=self.user_var, width=18).grid(row=0, column=5, padx=6)

        L(1,0,"Date From (YYYY-MM-DD):"); self.date_from_var = tk.StringVar(); ttk.Entry(filt, textvariable=self.date_from_var, width=18).grid(row=1, column=1, padx=6)
        L(1,2,"Date To (YYYY-MM-DD):");   self.date_to_var   = tk.StringVar(); ttk.Entry(filt, textvariable=self.date_to_var, width=18).grid(row=1, column=3, padx=6)

        L(2,0,"Sentiment:"); self.sentiment_var = tk.StringVar()
        self.sentiment_combo = ttk.Combobox(filt, textvariable=self.sentiment_var, values=["", "Positive", "Neutral", "Negative"], width=16)
        self.sentiment_combo.grid(row=2, column=1, padx=6); self.sentiment_combo.current(0)

        L(2,2,"Min Score:"); self.min_score_var = tk.StringVar(); ttk.Entry(filt, textvariable=self.min_score_var, width=10).grid(row=2, column=3, padx=6, sticky="w")
        L(2,4,"Max Score:"); self.max_score_var = tk.StringVar(); ttk.Entry(filt, textvariable=self.max_score_var, width=10).grid(row=2, column=5, padx=6, sticky="w")

        L(3,0,"Text contains:"); self.contains_var = tk.StringVar()
        ttk.Entry(filt, textvariable=self.contains_var, width=40).grid(row=3, column=1, columnspan=3, padx=6, sticky="we")

        btns = tk.Frame(filt, bg="#F3F4F6"); btns.grid(row=4, column=0, columnspan=6, sticky="w", pady=(8,4))
        ttk.Button(btns, text="Search", command=self.search).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Reset",  command=self.reset_filters).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Export CSV", command=self.export_csv).grid(row=0, column=2, padx=12)

        # Results
        table = tk.Frame(self, bg="#F3F4F6"); table.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # exact columns as in the screenshot
        self.columns = ("created_at", "keyword", "user", "run_id", "sentiment", "score", "text")
        self.tree = ttk.Treeview(table, columns=self.columns, show="headings", height=16)

        # widths & alignment (text stretches)
        setup = [
            ("created_at", 160, "w"),
            ("keyword",    140, "w"),
            ("user",       180, "w"),
            ("run_id",     280, "w"),
            ("sentiment",  100, "center"),
            ("score",       70, "center"),
            ("text",       800, "w"),
        ]
        for col, w, anchor in setup:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=w, anchor=anchor, stretch=(col == "text"))

        vsb = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=vsb.set); self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Pager
        pager = tk.Frame(self, bg="#F3F4F6"); pager.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=8)
        ttk.Button(pager, text="◀ Prev", command=self.prev_page).pack(side=tk.LEFT)
        ttk.Button(pager, text="Next ▶", command=self.next_page).pack(side=tk.LEFT, padx=6)
        self.count_label = tk.Label(pager, text="", bg="#F3F4F6"); self.count_label.pack(side=tk.RIGHT)

        self._load_runs_into_dropdown()
        self.search()

    # --- helpers (same logic you had, trimmed for space) ---
    def _load_runs_into_dropdown(self):
        cy = """MATCH (r:RUN) RETURN r.id AS id, r.keyword AS keyword, r.ts AS ts
                ORDER BY coalesce(r.ts, datetime()) DESC LIMIT 200"""
        recs,_,_ = self.driver.execute_query(cy)
        self.run_combo["values"] = [""] + [f"{r.get('keyword') or ''} • {r['id']}" for r in recs]

    def _parse_run_id(self, v): 
        return (v.split("•",1)[1] if "•" in v else v).strip() if v else None

    def _build_params(self):
        p = {
            "keyword": (self.keyword_var.get().strip() or None),
            "run_id": self._parse_run_id(self.run_var.get().strip()),
            "user": (self.user_var.get().strip() or None),
            "date_from": (self.date_from_var.get().strip() or None),
            "date_to": (self.date_to_var.get().strip() or None),
            "sentiment": (self.sentiment_var.get().strip() or None),
            "min_score": None, "max_score": None,
            "contains": (self.contains_var.get().strip().lower() or None),
            "skip": self.skip, "limit": self.limit,
        }
        try:
            if self.min_score_var.get().strip(): p["min_score"] = float(self.min_score_var.get())
            if self.max_score_var.get().strip(): p["max_score"] = float(self.max_score_var.get())
        except ValueError:
            messagebox.showerror("Input Error","Min/Max Score must be numbers.")
        return p

    def _query_count(self, params):
        cy = """
        MATCH (t:Tweet)
        OPTIONAL MATCH (t)-[:MENTIONS]->(k:Keyword)
        OPTIONAL MATCH (t)<-[:INGESTED]-(ing:USER)
        OPTIONAL MATCH (t)-[:BY|:AUTHORED_BY|:CREATED_BY]->(a)
        OPTIONAL MATCH (t)-[:OF_RUN]->(r:RUN)
        OPTIONAL MATCH (t)-[:HAS_CLEANED]->(c:CleanedTweet)
        WITH t,k,ing,a,r,c,
             toLower(coalesce(t.author_username,a.username,a.handle,a.screen_name,ing.username,'')) AS who,
             toLower(t.text) AS rawtxt,
             toLower(coalesce(c.cleaned,'')) AS cleantxt
        WHERE ($keyword  IS NULL OR toLower(k.name) CONTAINS toLower($keyword))
          AND ($run_id   IS NULL OR r.id = $run_id)
          AND ($user     IS NULL OR who CONTAINS toLower($user))
          AND ($contains IS NULL OR rawtxt CONTAINS $contains OR cleantxt CONTAINS $contains)
          AND ($date_from IS NULL OR t.created_at >= datetime($date_from))
          AND ($date_to   IS NULL OR t.created_at <  datetime($date_to) + duration('P1D'))
          AND ($sentiment IS NULL OR c.sentiment = $sentiment)
          AND ($min_score IS NULL OR c.score >= $min_score)
          AND ($max_score IS NULL OR c.score <= $max_score)
        RETURN count(*) AS n
        """
        recs,_,_ = self.driver.execute_query(cy, params); return recs[0]["n"]
    def _query_page(self, params):
        cy = """
        MATCH (t:Tweet)
        OPTIONAL MATCH (t)-[:MENTIONS]->(k:Keyword)
        OPTIONAL MATCH (t)<-[:INGESTED]-(ing:USER)
        OPTIONAL MATCH (t)-[:BY|:AUTHORED_BY|:CREATED_BY]->(a)
        OPTIONAL MATCH (t)-[:OF_RUN]->(r:RUN)
        OPTIONAL MATCH (t)-[:HAS_CLEANED]->(c:CleanedTweet)
        WITH t,k,ing,a,r,c,
            toLower(coalesce(t.author_username,a.username,a.handle,a.screen_name,ing.username,'')) AS who_lower,
            coalesce(t.author_username, a.username, a.handle, a.screen_name, ing.username, '')     AS user_display,
            toLower(t.text) AS rawtxt,
            toLower(coalesce(c.cleaned,'')) AS cleantxt
        WHERE ($keyword  IS NULL OR toLower(k.name) CONTAINS toLower($keyword))
        AND ($run_id   IS NULL OR r.id = $run_id)
        AND ($user     IS NULL OR who_lower CONTAINS toLower($user))
        AND ($contains IS NULL OR rawtxt CONTAINS $contains OR cleantxt CONTAINS $contains)
        AND ($date_from IS NULL OR t.created_at >= datetime($date_from))
        AND ($date_to   IS NULL OR t.created_at <  datetime($date_to) + duration('P1D'))
        AND ($sentiment IS NULL OR c.sentiment = $sentiment)
        AND ($min_score IS NULL OR c.score >= $min_score)
        AND ($max_score IS NULL OR c.score <= $max_score)
        RETURN
            t.created_at        AS created_at,
            coalesce(k.name,'') AS keyword,
            user_display        AS user,
            r.id                AS run_id,
            c.sentiment         AS sentiment,
            c.score             AS score,
            t.text              AS text
        ORDER BY t.created_at DESC
        SKIP $skip LIMIT $limit
        """
        recs,_,_ = self.driver.execute_query(cy, params)
        rows = []
        for r in recs:
            rows.append({
                "created_at": str(r.get("created_at") or ""),
                "keyword": r.get("keyword") or "",
                "user": r.get("user") or "",
                "run_id": r.get("run_id") or "",
                "sentiment": r.get("sentiment") or "",
                "score": r.get("score"),
                "text": r.get("text") or "",
            })
        return rows

    def _refresh_table(self, rows, start, end, total):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    r["created_at"],
                    r["keyword"],
                    r["user"],
                    r["run_id"],
                    r["sentiment"],
                    r["score"],
                    r["text"],
                ),
            )
        self.count_label.config(text=f"Showing {start}-{end} of {total}")

    # public
    def search(self):
        self.skip = 0
        p = self._build_params(); total = self._query_count(p)
        rows = self._query_page(p)
        start = (p["skip"] + 1) if total > 0 else 0; end = min(p["skip"] + self.limit, total)
        self._refresh_table(rows, start, end, total)

    def next_page(self):
        p = self._build_params(); total = self._query_count(p)
        if self.skip + self.limit < total:
            self.skip += self.limit; p["skip"] = self.skip
            rows = self._query_page(p); start = p["skip"] + 1; end = min(p["skip"] + self.limit, total)
            self._refresh_table(rows, start, end, total)

    def prev_page(self):
        if self.skip >= self.limit: self.skip -= self.limit
        else: self.skip = 0
        p = self._build_params(); total = self._query_count(p); p["skip"] = self.skip
        rows = self._query_page(p); start = p["skip"] + 1 if total>0 else 0; end = min(p["skip"] + self.limit, total)
        self._refresh_table(rows, start, end, total)

    def reset_filters(self):
        for var in [self.keyword_var, self.run_var, self.user_var, self.date_from_var, self.date_to_var, self.sentiment_var, self.min_score_var, self.max_score_var, self.contains_var]:
            var.set("")
        self.skip = 0; self.search()

    def export_csv(self):
        p = self._build_params(); p["skip"]=0; p["limit"]=100000
        rows = self._query_page(p)
        if not rows:
            return messagebox.showinfo("Export","No rows to export.")
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV","*.csv")],
            title="Save history as CSV"
        )
        if not path:
            return
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Created At","Keyword","User","Run ID","Sentiment","Score","Text"])
            for r in rows:
                w.writerow([r["created_at"], r["keyword"], r["user"], r["run_id"],
                            r["sentiment"], r["score"], r["text"]])
        messagebox.showinfo("Export", f"Saved {len(rows)} rows to {path}")

    def destroy(self):
        try: self.driver.close()
        except Exception: pass
        return super().destroy()