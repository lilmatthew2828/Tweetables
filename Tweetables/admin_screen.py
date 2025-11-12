# Brian Csehoski - Whole File

import tkinter as tk
from neo4j import GraphDatabase

URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

class AdminScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Screen")

        self.master.geometry("960x780")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Welcome to the Admin Screen", font=("Helvetica", 24), bg="#ADD8E6").pack(pady=20)

        text_frame = tk.Frame(self.frame)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Arial", 12), yscrollcommand=scrollbar.set)
        # match the mono/clean aesthetic
        self.output_text.configure(font=("Consolas", 11), background="#FFFFFF", foreground="#111827", insertbackground="#111827", relief=tk.FLAT, bd=0)

        # pretty styling tags to mirror the newer GUI
        self.output_text.tag_config("dim", foreground="#6b7280")      # gray-500
        self.output_text.tag_config("label", foreground="#374151", font=("Consolas", 11, "bold"))
        self.output_text.tag_config("pos", foreground="#1b5e20")      # green-900
        self.output_text.tag_config("neu", foreground="#1e40af")      # blue-900
        self.output_text.tag_config("neg", foreground="#7f1d1d")      # red-900
        self.output_text.tag_config("sep", foreground="#9ca3af")      # divider
        self.output_text.tag_config("mono", font=("Consolas", 11))
        self.output_text.tag_config("pad",  lmargin1=8,  lmargin2=8)
        self.output_text.tag_config("pad2", lmargin1=20, lmargin2=20)
        # extra tags used by headings/badges
        self.output_text.tag_config("h2", font=("Arial", 13, "bold"))
        self.output_text.tag_config("badge_pos", foreground="#1b5e20")
        self.output_text.tag_config("badge_neu", foreground="#1e40af")
        self.output_text.tag_config("badge_neg", foreground="#7f1d1d")

        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)


        def retrieve_unscored_tweets(driver):
            query = """
            MATCH (u:UNSCORED_WORD)
            RETURN u.word AS word, u.frequency AS frequency
            """
            
            records, _, _ = driver.execute_query(query)
            return records
        
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            self.unscored_tweets = retrieve_unscored_tweets(driver)
            driver.close()
        

        for word, frequency in self.unscored_tweets:
            self.output_text.insert(tk.END, f"Word: {word} | Frequency: {frequency}\n", ("mono", "pad"))



if __name__ == "__main__":
    root = tk.Tk()
    app = AdminScreen(root)
    root.mainloop()