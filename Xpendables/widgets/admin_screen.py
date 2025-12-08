# widgets/admin_screen.py
# Brian Csehoski - tweaked for new modular app

import tkinter as tk
from tkinter import ttk
from neo4j import GraphDatabase
from settings import URI, AUTH   # <-- use shared settings


class AdminScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)              # this *is* the window now
        self.title("Admin Screen")
        self.geometry("600x500")
        self.configure(bg="#000000")

        self.frame = tk.Frame(self, bg="#000000", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(
            self.frame,
            text="Welcome to the Admin Screen",
            font=("Helvetica", 24),
            bg="#000000"
        ).pack(pady=20)

        # --- control row with combobox for view selection ---
        control_frame = tk.Frame(self.frame, bg="#000000")
        control_frame.pack(fill=tk.X, pady=(0, 10))

        self.view_combo = ttk.Combobox(
            control_frame,
            values=["Original", "Ascending Frequency", "Descending Frequency"],
            state="readonly",
            width=24,
        )
        self.view_combo.current(0)
        self.view_combo.pack(side=tk.TOP, padx=8)
        self.view_combo.bind("<<ComboboxSelected>>",
                             lambda e: self.refresh_output())

        # --- text area + scrollbar ---
        text_frame = tk.Frame(self.frame, bg="#000000")
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=12,
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
            background="#000000",
            foreground="#FFFFFF",
            insertbackground="#111827",
            relief=tk.FLAT,
            bd=0,
        )

        # styling tags
        self.output_text.tag_config("dim", foreground="#6b7280")
        self.output_text.tag_config("label", foreground="#374151",
                                    font=("Consolas", 11, "bold"))
        self.output_text.tag_config("pos", foreground="#1b5e20")
        self.output_text.tag_config("neu", foreground="#1e40af")
        self.output_text.tag_config("neg", foreground="#7f1d1d")
        self.output_text.tag_config("sep", foreground="#9ca3af")
        self.output_text.tag_config("mono", font=("Consolas", 11))
        self.output_text.tag_config("pad",  lmargin1=8,  lmargin2=8)
        self.output_text.tag_config("pad2", lmargin1=20, lmargin2=20)
        self.output_text.tag_config("h2", font=("Arial", 13, "bold"))
        self.output_text.tag_config("badge_pos", foreground="#1b5e20")
        self.output_text.tag_config("badge_neu", foreground="#1e40af")
        self.output_text.tag_config("badge_neg", foreground="#7f1d1d")

        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # ---- load data from Neo4j ----
        def retrieve_unscored_tweets(driver):
            query = """
            MATCH (u:UNSCORED_WORD)
            RETURN u.word AS word, u.frequency AS frequency
            """
            records, _, _ = driver.execute_query(query)
            # return list of (word, frequency) tuples
            return [(r["word"], r["frequency"]) for r in records]

        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            self.unscored_tweets = retrieve_unscored_tweets(driver)

        # pre-sorted views
        self.unscored_tweets_ascending = sorted(
            self.unscored_tweets, key=lambda wf: wf[1]
        )
        self.unscored_tweets_descending = sorted(
            self.unscored_tweets, key=lambda wf: wf[1], reverse=True
        )

        # initial display
        self.output_text.config(state=tk.NORMAL)
        for word, frequency in self.unscored_tweets:
            self.output_text.insert(
                tk.END,
                f"Word: {word} | Frequency: {frequency}\n",
                ("mono", "pad"),
            )
        self.output_text.config(state=tk.DISABLED)

    # refresh handler for combobox
    def refresh_output(self):
        selection = self.view_combo.get()
        if selection == "Original":
            data = self.unscored_tweets
        elif selection == "Ascending Frequency":
            data = self.unscored_tweets_ascending
        else:
            data = self.unscored_tweets_descending

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        for word, frequency in data:
            self.output_text.insert(
                tk.END,
                f"Word: {word} | Frequency: {frequency}\n",
                ("mono", "pad"),
            )
        self.output_text.config(state=tk.DISABLED)



if __name__ == "__main__":
    root = tk.Tk()
    app = AdminScreen(root)
    root.mainloop()