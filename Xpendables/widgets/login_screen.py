# widgets/login_screen.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import bcrypt
from neo4j import GraphDatabase

from settings import LOGO_PATH, URI, AUTH
from app_state import state

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("550x650")
        self.master.configure(bg="#000000")

        # ----- ttk DARK THEME STYLING -----
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
        self.frame.pack(expand=True)

        # Logo
        try:
            self.logo_photo = ImageTk.PhotoImage(Image.open(LOGO_PATH).resize((150,150)))
            tk.Label(self.frame, image=self.logo_photo, bg="#ADD8E6")\
                .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        except Exception as e:
            print("Logo load error:", e)

        # Form
        ttk.Label(self.frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(self.frame, font=("Arial", 12), width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(self.frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(self.frame, font=("Arial", 12), show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)

        self.message_label = ttk.Label(self.frame, text="", foreground="#FFFFFF")
        self.message_label.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(self.frame, text="Login", command=self.validate_login)\
          .grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(self.frame, text="Sign Up", command=self.open_signup)\
          .grid(row=5, column=0, columnspan=2, pady=10)

    # --- actions ---
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if self.check_credentials(username, password):
            self.message_label.config(text="Login successful!", foreground="#FFFFFF")
            state.CURRENT_USER = username
            if username == "admin":
                self.open_admin_screen()
            else:
                self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Username or password is wrong", foreground="#FFFFFF")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def check_credentials(self, username, password):
        pw_bytes = password.encode("utf-8")

        def get_hash(driver):
            q = "MATCH (u:USER {username:$u}) RETURN u.hashed_password AS hp"
            recs, _, _ = driver.execute_query(q, u=username)
            if not recs:
                return None
            return recs[0]["hp"]

        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            hashed = get_hash(driver)
        return bool(hashed and bcrypt.checkpw(pw_bytes, hashed))

    def open_signup(self):
        # lazy import to avoid circulars
        from widgets.signup_window import SignupWindow
        SignupWindow(self.master)

    def open_sentiment_analysis(self):
        from widgets.sentiment_app import SentimentAnalysisApp
        self.master.destroy()
        root = tk.Tk()
        SentimentAnalysisApp(root)
        root.mainloop()

    def open_admin_screen(self):
        from widgets.admin_screen import AdminScreen
        self.master.destroy()
        AdminScreen()

