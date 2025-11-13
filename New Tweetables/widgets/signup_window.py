# widgets/signup_window.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import tweepy, bcrypt, os
from cryptography.fernet import Fernet
from neo4j import GraphDatabase
from dotenv import load_dotenv

from settings import LOGO_PATH, URI, AUTH

load_dotenv()

class SignupWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master)
        self.win.title("Sign Up")
        self.win.geometry("450x520")
        self.win.configure(bg="#ADD8E6")

        frame = tk.Frame(self.win, bg="#ADD8E6", padx=20, pady=20)
        frame.pack(expand=True)

        # Logo
        try:
            self.logo_photo = ImageTk.PhotoImage(
                Image.open(LOGO_PATH).resize((140, 140))
            )
            tk.Label(frame, image=self.logo_photo, bg="#ADD8E6")\
              .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        except Exception as e:
            print("Signup logo error:", e)

        # Fields
        row = 1
        def L(txt):
            nonlocal row
            tk.Label(frame, text=txt, font=("Arial", 12), bg="#ADD8E6")\
              .grid(row=row, column=0, sticky="w", pady=5)

        L("New Username:");   username = tk.Entry(frame, font=("Arial", 12)); username.grid(row=row, column=1, padx=10); row += 1
        L("New Password:");   pw1      = tk.Entry(frame, show="*", font=("Arial", 12)); pw1.grid(row=row, column=1, padx=10); row += 1
        L("Re-enter Password:"); pw2   = tk.Entry(frame, show="*", font=("Arial", 12)); pw2.grid(row=row, column=1, padx=10); row += 1

        L("API Key:");        api_key  = tk.Entry(frame, show="*", font=("Arial", 12)); api_key.grid(row=row, column=1, padx=10); row += 1
        L("API Secret:");     api_sec  = tk.Entry(frame, show="*", font=("Arial", 12)); api_sec.grid(row=row, column=1, padx=10); row += 1
        L("Access Token:");   acc_tok  = tk.Entry(frame, show="*", font=("Arial", 12)); acc_tok.grid(row=row, column=1, padx=10); row += 1
        L("Access Secret:");  acc_sec  = tk.Entry(frame, show="*", font=("Arial", 12)); acc_sec.grid(row=row, column=1, padx=10); row += 1
        L("Bearer Token:");   bearer   = tk.Entry(frame, show="*", font=("Arial", 12)); bearer.grid(row=row, column=1, padx=10); row += 1

        def save():
            u = username.get().strip()
            p1 = pw1.get()
            p2 = pw2.get()

            if not u or not p1:
                return messagebox.showerror("Error", "Username and password are required.")
            if "," in u or "," in p1:
                return messagebox.showerror("Error", "No commas allowed.")
            if p1 != p2:
                return messagebox.showerror("Error", "Passwords do not match.")

            # Ensure encryption key exists
            key = os.getenv("MASTER_KEY")
            if not key:
                return messagebox.showerror("Error", "MASTER_KEY is missing from environment.")
            try:
                f = Fernet(key.encode())
            except Exception as e:
                return messagebox.showerror("Error", f"MASTER_KEY invalid: {e}")

            # Check existing user
            with GraphDatabase.driver(URI, auth=AUTH) as drv:
                drv.verify_connectivity()
                recs, _, _ = drv.execute_query(
                    "MATCH (u:USER {username:$u}) RETURN count(u) AS n",
                    u=u
                )
                if recs[0]["n"] > 0:
                    return messagebox.showerror("Error", "Username already exists.")

            # Verify Twitter creds
            auth = tweepy.OAuthHandler(api_key.get(), api_sec.get())
            auth.set_access_token(acc_tok.get(), acc_sec.get())
            api = tweepy.API(auth, wait_on_rate_limit=True)
            try:
                api.verify_credentials()
            except Exception as e:
                return messagebox.showerror("Error", f"Twitter auth failed: {e}")

            # Hash + encrypt
            hashed = bcrypt.hashpw(p1.encode("utf-8"), bcrypt.gensalt())
            enc = lambda s: f.encrypt((s or "").encode())

            params = {
                "u": u,
                "hp": hashed,
                "ak": enc(api_key.get()),
                "asec": enc(api_sec.get()),
                "atok": enc(acc_tok.get()),
                "asecret": enc(acc_sec.get()),
                "bt": enc(bearer.get()),
            }

            cypher = """
            CREATE (u:USER {
                username:$u, hashed_password:$hp,
                enc_api_key:$ak, enc_api_secret:$asec,
                enc_access_token:$atok, enc_access_secret:$asecret,
                enc_bearer_token:$bt
            })
            WITH u
            MERGE (y:USERS)
            MERGE (u)-[:IS_A]->(y)
            """

            with GraphDatabase.driver(URI, auth=AUTH) as drv:
                drv.verify_connectivity()
                drv.execute_query(cypher, parameters=params)

            messagebox.showinfo("Success", "Account created. You can log in now.")
            self.win.destroy()

        tk.Button(
            frame, text="Sign Up", command=save,
            font=("Arial", 12), bg="white", fg="black", padx=10, pady=5
        ).grid(row=row, column=0, columnspan=2, pady=10)