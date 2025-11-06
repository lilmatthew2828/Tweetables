import tkinter as tk
from neo4j import GraphDatabase

class AdminScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Screen")

        self.master.geometry("960x780")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Welcome to the Admin Screen", font=("Helvetica", 24), bg="#ADD8E6").pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminScreen(root)
    root.mainloop()