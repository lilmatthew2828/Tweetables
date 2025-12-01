# widgets/login_screen.py
import tkinter as tk
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
        self.master.configure(bg="#00BFFF")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True)

        # Logo
        try:
            self.logo_photo = ImageTk.PhotoImage(Image.open(LOGO_PATH).resize((150,150)))
            tk.Label(self.frame, image=self.logo_photo, bg="#ADD8E6")\
                .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        except Exception as e:
            print("Logo load error:", e)

        # Form
        tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ADD8E6")\
          .grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ADD8E6")\
          .grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)

        self.message_label = tk.Label(self.frame, text="", fg="red", bg="#ADD8E6", font=("Arial", 10))
        self.message_label.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(self.frame, text="Login", command=self.validate_login,
                  font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)\
          .grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(self.frame, text="Sign Up", command=self.open_signup,
                  font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)\
          .grid(row=5, column=0, columnspan=2, pady=10)

    # --- actions ---
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if self.check_credentials(username, password):
            self.message_label.config(text="Login successful!", fg="green")
            state.CURRENT_USER = username
            self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Username or password is wrong", fg="red")
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

