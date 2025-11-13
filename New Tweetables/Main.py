# import tkinter as tk
# import threading
# import subprocess
# import os
# import sys
# import tkinter.messagebox
# from neo4j import GraphDatabase
# import tweepy
# import bcrypt
# from cryptography.fernet import Fernet
# from dotenv import load_dotenv
# import re
# # NEW IMPORTS
# import tkinter.ttk as ttk
# from tkinter import filedialog, messagebox
# #new import for image on login screen
# from PIL import Image, ImageTk

# load_dotenv()

# # USER.TXT IS MASSIVELY IMPORTANT FOR LOGGING IN.
# # MY GOAL IS TOO MAKE SO IT CAN HOLD A NUMBER OF VARIOUS POSSIBLE LOGIN CREDNETIALS TOO MAKE THIS MORE REALISTIC
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# USERS_FILE = os.path.join(BASE_DIR, "users.txt")
# # Make subprocess I/O deterministic across macOS/Windows/VS Code
# SCRIPT_DIR = BASE_DIR  # folder containing this Main.py and the other scripts
# NLTK_DIR = os.path.join(SCRIPT_DIR, "nltk_data")
# os.makedirs(NLTK_DIR, exist_ok=True)

# # We will evenutally need to remove this and like save it somewhere safe but these are here for now
# URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
# AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

# CURRENT_USER = None


# def _subprocess_env():
#     # Add NLTK_DATA so both child scripts find/download data in-project
#     env = {**os.environ, "NLTK_DATA": NLTK_DIR}
#     return env


# class LoginScreen:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Login")
#         self.master.geometry("550x650")
#         self.master.configure(bg="#00BFFF")

#         self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
#         self.frame.pack(expand=True)

#         # Load and display the image
#         try:
#             logo_path = os.path.join(BASE_DIR, "unnamed.png")
#             logo_img = Image.open(logo_path).resize((150, 150))  # a bit larger looks nicer
#             self.logo_photo = ImageTk.PhotoImage(logo_img)
#             tk.Label(self.frame, image=self.logo_photo, bg="#ADD8E6")\
#                 .grid(row=0, column=0, columnspan=2, pady=(0, 20))
#         except Exception as e:
#             print(f"Error loading logo image: {e}")

#         # 👇 Shift everything down by +1
#         tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=1, column=0, sticky="w", pady=5)
#         self.username_entry = tk.Entry(self.frame, font=("Arial", 12))
#         self.username_entry.grid(row=1, column=1, pady=5, padx=10)

#         tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=2, column=0, sticky="w", pady=5)
#         self.password_entry = tk.Entry(self.frame, font=("Arial", 12), show="*")
#         self.password_entry.grid(row=2, column=1, pady=5, padx=10)

#         self.message_label = tk.Label(self.frame, text="", fg="red", bg="#ADD8E6", font=("Arial", 10))
#         self.message_label.grid(row=3, column=0, columnspan=2, pady=5)

#         self.login_button = tk.Button(self.frame, text="Login", command=self.validate_login,
#                                     font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
#         self.login_button.grid(row=4, column=0, columnspan=2, pady=10)

#         self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup,
#                                     font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
#         self.signup_button.grid(row=5, column=0, columnspan=2, pady=10)

#     def validate_login(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()

#         if self.check_credentials(username, password):
#             self.message_label.config(text="Login successful!", fg="green")
#             global CURRENT_USER
#             CURRENT_USER = username
#             self.open_sentiment_analysis()
#         else:
#             self.message_label.config(text="Username or password is wrong", fg="red")
#             self.username_entry.delete(0, tk.END)
#             self.password_entry.delete(0, tk.END)

#     def check_credentials(self, username, password):  # Fixed This as well You hit this because some lines in users.txt have more than one comma, so
#         passwordBytes = password.encode('utf-8')

#         def check_credentials2(driver, username):
#             query = """
#                 MATCH (u:USER {username: $username})
#                 RETURN u.hashed_password AS user_password
#             """
#             records, summary, key = driver.execute_query(query, username=username)
#             if records == []:
#                 return False
#             return bcrypt.checkpw(passwordBytes, records[0]["user_password"])

#         with GraphDatabase.driver(URI, auth=AUTH) as driver:
#             driver.verify_connectivity()
#             value = check_credentials2(driver, username)
#             driver.close()

#         return value

#     def open_signup(self):  # method for user sign up process. Needs ode tweaking
#         signup_window = tk.Toplevel(self.master)
#         signup_window.title("Sign Up")
#         signup_window.geometry("450x450")
#         signup_window.configure(bg="#ADD8E6")
    
#         frame = tk.Frame(signup_window, bg="#ADD8E6", padx=20, pady=20)
#         frame.pack(expand=True)
#         # NEW -  Add logo to Sign-Up screen
#         try:
#             logo_path = os.path.join(BASE_DIR, "unnamed.png")
#             logo_img = Image.open(logo_path).resize((140, 140))
#             self.signup_logo_photo = ImageTk.PhotoImage(logo_img)
#             tk.Label(frame, image=self.signup_logo_photo, bg="#ADD8E6")\
#                 .grid(row=0, column=0, columnspan=2, pady=(0, 20))
#         except Exception as e:
#             print(f"Signup logo load error: {e}")

#         # Shift all fields down by +1 (start at row=1)
#         tk.Label(frame, text="New Username:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=1, column=0, sticky="w", pady=5)
#         new_username = tk.Entry(frame, font=("Arial", 12))
#         new_username.grid(row=1, column=1, pady=5, padx=10)

#         tk.Label(frame, text="New Password:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=2, column=0, sticky="w", pady=5)
#         new_password = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_password.grid(row=2, column=1, pady=5, padx=10)

#         tk.Label(frame, text="Re-enter New Password:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=3, column=0, sticky="w", pady=5)
#         new_password_again = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_password_again.grid(row=3, column=1, pady=5, padx=10)

#         tk.Label(frame, text="Enter API Key:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=4, column=0, sticky="w", pady=5)
#         new_api_key = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_api_key.grid(row=4, column=1, pady=5, padx=10)

#         tk.Label(frame, text="Enter API Secret:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=5, column=0, sticky="w", pady=5)
#         new_api_secret = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_api_secret.grid(row=5, column=1, pady=5, padx=10)

#         tk.Label(frame, text="Enter Access Token:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=6, column=0, sticky="w", pady=5)
#         new_access_token = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_access_token.grid(row=6, column=1, pady=5, padx=10)

#         tk.Label(frame, text="Enter Access Secret:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=7, column=0, sticky="w", pady=5)
#         new_access_secret = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_access_secret.grid(row=7, column=1, pady=5, padx=10)

#         tk.Label(frame, text="Enter Bearer Token:", font=("Arial", 12), bg="#ADD8E6")\
#         .grid(row=8, column=0, sticky="w", pady=5)
#         new_bearer_token = tk.Entry(frame, font=("Arial", 12), show="*")
#         new_bearer_token.grid(row=8, column=1, pady=5, padx=10)

#         # Move Sign Up button to the next row (row 9)
#         signup_button = tk.Button(frame, text="Sign Up", command=save_credentials,
#                                 font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
#         signup_button.grid(row=9, column=0, columnspan=2, pady=10)

#         # =========================================================================================================================================================================================
#         def save_credentials():
#             username = new_username.get()
#             password = new_password.get()

#             # Basic validation
#             if not username or not password:
#                 tk.messagebox.showerror("Error", "Username and password are required.")
#                 return
#             if "," in username or "," in password:
#                 tk.messagebox.showerror("Error", "Commas are not allowed in username or password.")
#                 return

#             # Fucntion to check if username already exists in the database
#             def check_exists(driver, username):
#                 query = """
#                     MATCH (u:USER {username: $username})
#                     RETURN COUNT(u) AS user_count
#                     """
#                 records, summary, key = driver.execute_query(query, username=username)
#                 existing = records[0]["user_count"]
#                 if existing == 0:
#                     return False
#                 else:
#                     return True

#             # Execute the query to check for existing username
#             with GraphDatabase.driver(URI, auth=AUTH) as driver:
#                 driver.verify_connectivity()
#                 if check_exists(driver, username):
#                     tk.messagebox.showerror("Error", "Username already exists.")
#                     return
#                 driver.close()

#             # Check if passwords match
#             if password != new_password_again.get():
#                 tk.messagebox.showerror("Error", "Passwords do not match.")
#                 return

#             api_key = new_api_key.get()
#             api_secret = new_api_secret.get()
#             access_token = new_access_token.get()
#             access_secret = new_access_secret.get()
#             bearer_token = new_bearer_token.get()

#             # Validate Twitter API credentials
#             auth = tweepy.OAuthHandler(api_key, api_secret)
#             auth.set_access_token(access_token, access_secret)

#             api = tweepy.API(auth, wait_on_rate_limit=True)

#             try:
#                 api.verify_credentials()
#             except Exception as e:
#                 tk.messagebox.showerror("Error", f"Twitter API authentication failed: {e}")
#                 return

#             # Encrypt password before saving with one-way bcrypt hashing
#             bytes_pw = password.encode('utf-8')
#             salt = bcrypt.gensalt()
#             hashed_password = bcrypt.hashpw(bytes_pw, salt)

#             # Encrypt all API credentials before saving with two-way Fernet encryption
#             key = os.getenv("MASTER_KEY")
#             f = Fernet(key)
#             enc_api_key = f.encrypt(api_key.encode())
#             enc_api_secret = f.encrypt(api_secret.encode())
#             enc_access_token = f.encrypt(access_token.encode())
#             enc_access_secret = f.encrypt(access_secret.encode())
#             enc_bearer_token = f.encrypt(bearer_token.encode())

#             # Create the function to add new user to the database
#             def create_account(driver, username, hashed_password, enc_api_key, enc_api_secret, enc_access_token, enc_access_secret, enc_bearer_token):
#                 query = """
#                     CREATE (u:USER {username: $username, hashed_password: $hashed_password, enc_api_key: $enc_api_key, enc_api_secret: $enc_api_secret, enc_access_token: $enc_access_token, enc_access_secret: $enc_access_secret, enc_bearer_token: $enc_bearer_token})
#                     WITH u
#                     MATCH (y:USERS)
#                     MERGE (u)-[:IS_A]->(y)
#                 """
#                 driver.execute_query(query, username=username, hashed_password=hashed_password, enc_api_key=enc_api_key, enc_api_secret=enc_api_secret, enc_access_token=enc_access_token, enc_access_secret=enc_access_secret, enc_bearer_token=enc_bearer_token)

#             # Run the function to create the account
#             with GraphDatabase.driver(URI, auth=AUTH) as driver:
#                 driver.verify_connectivity()
#                 create_account(driver, username, hashed_password, enc_api_key, enc_api_secret, enc_access_token, enc_access_secret, enc_bearer_token)
#                 driver.close()

#             tk.messagebox.showinfo("Success", "Account created. You can log in now.")
#             signup_window.destroy()

#         signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
#         signup_button.grid(row=8, columnspan=2, pady=10)
#         # =========================================================================================================================================================================================

#     def open_sentiment_analysis(self):
#         self.master.destroy()
#         root = tk.Tk()
#         app = SentimentAnalysisApp(root)
#         root.mainloop()


# class SentimentAnalysisApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Xpendables: Sentiment Analysis")
#         # match updated GUI sizing/look
#         self.master.geometry("960x780")
#         self.master.configure(bg="#ADD8E6")

#         self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
#         self.frame.pack(expand=True, fill=tk.BOTH)

#         tk.Label(self.frame, text="Xpendables: Movie Sentiment Analysis Tool", font=("Helvetica", 16, "bold"), bg="#ADD8E6").pack(pady=10)

#         # --- keyword entry box ---
#         keyword_frame = tk.Frame(self.frame, bg="#ADD8E6")
#         keyword_frame.pack(pady=5)
#         tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
#         self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
#         self.keyword_entry.pack(side=tk.LEFT, padx=5)

#         # --- output text box with scrollbar ---
#         text_frame = tk.Frame(self.frame)
#         text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
#         scrollbar = tk.Scrollbar(text_frame)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Arial", 12), yscrollcommand=scrollbar.set)
#         # match the mono/clean aesthetic
#         self.output_text.configure(font=("Consolas", 11), background="#FFFFFF", foreground="#111827", insertbackground="#111827", relief=tk.FLAT, bd=0)

#         # pretty styling tags to mirror the newer GUI
#         self.output_text.tag_config("dim", foreground="#6b7280")      # gray-500
#         self.output_text.tag_config("label", foreground="#374151", font=("Consolas", 11, "bold"))
#         self.output_text.tag_config("pos", foreground="#1b5e20")      # green-900
#         self.output_text.tag_config("neu", foreground="#1e40af")      # blue-900
#         self.output_text.tag_config("neg", foreground="#7f1d1d")      # red-900
#         self.output_text.tag_config("sep", foreground="#9ca3af")      # divider
#         self.output_text.tag_config("mono", font=("Consolas", 11))
#         self.output_text.tag_config("pad",  lmargin1=8,  lmargin2=8)
#         self.output_text.tag_config("pad2", lmargin1=20, lmargin2=20)
#         # extra tags used by headings/badges
#         self.output_text.tag_config("h2", font=("Arial", 13, "bold"))
#         self.output_text.tag_config("badge_pos", foreground="#1b5e20")
#         self.output_text.tag_config("badge_neu", foreground="#1e40af")
#         self.output_text.tag_config("badge_neg", foreground="#7f1d1d")

#         self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.config(command=self.output_text.yview)

#         # sentiment counters to support the badge summary
#         self._counts = {"positive": 0, "neutral": 0, "negative": 0}

#         # --- buttons ---
#         btn_frame = tk.Frame(self.frame, bg="#ADD8E6")
#         btn_frame.pack(pady=10)

#         self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets,
#                                        font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
#         self.search_button.grid(row=0, column=0, padx=5)

#         self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis,
#                                          font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
#         self.analysis_button.grid(row=0, column=1, padx=5)

#         self.full_run_button = tk.Button(
#             btn_frame,
#             text="Run Full Analysis",
#             command=self.run_full_pipeline,
#             font=("Arial", 12), bg="white", fg="black", padx=10, pady=5
#         )
#         self.full_run_button.grid(row=1, column=0, columnspan=2, pady=8)

#         self.history_button = tk.Button( # <— new button
#             btn_frame,
#             text="History",
#             command=self.open_history_viewer,   # <— points to method below
#             font=("Arial", 12), bg="white", fg="black", padx=10, pady=5
#         )
#         self.history_button.grid(row=2, column=0, columnspan=2, pady=8)
        
#     # ===== GUI-look helper methods (purely visual) =====
#     def _append(self, text: str, *tags):
#         if tags:
#             self.output_text.insert(tk.END, text, tags)
#         else:
#             self.output_text.insert(tk.END, text)
#         self.output_text.see(tk.END)

#     def _append_line(self, text: str = "", *tags):
#         self._append(text + "\n", *tags)

#     def _divider(self, label: str | None = None):
#         line = "─" * 60
#         if label:
#             pad = max(1, (60 - len(label) - 2) // 2)
#             line = f"{'─'*pad} {label} {'─'*pad}"
#         self._append_line(line, "sep")

#     def _heading(self, text: str):
#         self._append_line(text, "h2")

#     def _badge_summary(self):
#         p = self._counts["positive"]
#         n = self._counts["neutral"]
#         g = self._counts["negative"]
#         self._append("  ")
#         self._append(f"● {p} positive", "badge_pos")
#         self._append("   ")
#         self._append(f"● {n} neutral", "badge_neu")
#         self._append("   ")
#         self._append(f"● {g} negative", "badge_neg")
#         self._append_line()

#     def _clear_output(self):
#         self.output_text.delete("1.0", tk.END)
#         self._counts = {"positive": 0, "neutral": 0, "negative": 0}

#     def _thick_divider(self, label: str | None = None):
#         line = "═" * 78
#         if label:
#             pad = max(1, (78 - len(label) - 2) // 2)
#             line = f"{'═'*pad} {label} {'═'*pad}"
#         self.output_text.insert(tk.END, line + "\n", ("sep", "mono"))
#         self.output_text.see(tk.END)

#     def _emit_block(self, raw: str | None, cleaned: str | None, sent: str | None, score: float | None):
#         if not any([raw, cleaned, sent]):
#             return
#         s = (sent or "neutral").lower()
#         tag = {"positive": "pos", "negative": "neg", "neutral": "neu"}.get(s, "neu")

#         # header
#         self.output_text.insert(tk.END, "● ", (tag, "pad", "mono"))
#         self.output_text.insert(tk.END, (sent or "Neutral").title(), (tag, "mono"))
#         if score is not None:
#             self.output_text.insert(tk.END, f"  (score: {score})", ("dim", "mono"))
#         self.output_text.insert(tk.END, "\n", ("mono",))

#         if raw is not None:
#             self.output_text.insert(tk.END, "RAW: ", ("label", "pad2", "mono"))
#             self.output_text.insert(tk.END, raw.strip() + "\n", ("mono",))
#         if cleaned is not None:
#             self.output_text.insert(tk.END, "CLEANED: ", ("label", "pad2", "mono"))
#             self.output_text.insert(tk.END, (cleaned.strip() or "—") + "\n", ("mono",))
#         if sent is not None:
#             self.output_text.insert(tk.END, "SENTIMENT: ", ("label", "pad2", "mono"))
#             txt = sent.title() + (f"  (score: {score})" if score is not None else "")
#             self.output_text.insert(tk.END, txt + "\n", (tag, "mono"))

#         self.output_text.insert(tk.END, "\n", ("mono",))
#         self._thick_divider()

#     def _pretty_ingest_line(self, line: str):
#         """Collect RAW/CLEANED/SENTIMENT lines and render them as one styled block."""
#         if not hasattr(self, "_blk"):
#             self._blk = {"raw": None, "cleaned": None, "sent": None, "score": None}

#         s = line.strip()

#         if s.startswith("RAW:"):
#             self._blk = {"raw": s[4:].strip(), "cleaned": None, "sent": None, "score": None}
#             return

#         if s.startswith("CLEANED:"):
#             if self._blk.get("raw") is not None:
#                 self._blk["cleaned"] = s[8:].strip()
#             return

#         if "SENTIMENT:" in s:
#             m_sent = re.search(r"SENTIMENT:\s*([A-Za-z]+)", s)
#             m_score = re.search(r"Score:\s*([+-]?\d*\.?\d+)", s)
#             self._blk["sent"] = (m_sent.group(1) if m_sent else "Neutral")
#             self._blk["score"] = float(m_score.group(1)) if m_score else None
#             return

#         # dashed line between tweets flushes a block
#         if set(s) == {"-"}:
#             self._emit_block(self._blk.get("raw"), self._blk.get("cleaned"), self._blk.get("sent"), self._blk.get("score"))
#             final_sent = (self._blk.get("sent") or "neutral").lower()
#             if final_sent in self._counts:
#                 self._counts[final_sent] += 1
#             self._blk = {"raw": None, "cleaned": None, "sent": None, "score": None}
#             return

#         # any other line → dim log
#         self.output_text.insert(tk.END, s + "\n", ("dim", "pad", "mono"))
#         self.output_text.see(tk.END)
#     def open_history(self):
#         try:
#             HistoryWindow(self.master, CURRENT_USER)
#         except Exception as e:
#             self.append_output(f"Could not open history: {e}")
#     # ===== Threads / pipeline =====
#     def run_full_pipeline(self):
#         threading.Thread(target=self._run_pipeline_thread, daemon=True).start()

#     def _run_pipeline_thread(self):
#         keyword = self.keyword_entry.get().strip()
#         if not keyword:
#             self.master.after(0, self.append_output, "Please enter a movie keyword first.")
#             return

#         fetch_path = os.path.join(SCRIPT_DIR, "fetch_tweets.py")
#         analyze_path = os.path.join(SCRIPT_DIR, "analyze_sentiment.py")
#         raw_path = os.path.join(SCRIPT_DIR, "raw_tweets.txt")

#         try:
#             # match newer GUI: clear + header + divider
#             self.master.after(0, self._clear_output)
#             self.master.after(0, self._heading, "Full Analysis")
#             self.master.after(0, self._divider, "Fetch")

#             # --- Step 1: Fetch Tweets ---
#             self.master.after(0, self.append_output, f"Fetching tweets for '{keyword}'...")
#             fetch_process = subprocess.Popen(
#                 [sys.executable, fetch_path, keyword, CURRENT_USER],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 cwd=SCRIPT_DIR,  # ensure consistent read/write folder
#                 env=_subprocess_env(),  # pass NLTK_DATA, etc.
#             )

#             for line in fetch_process.stdout:
#                 self.master.after(0, self.append_output, line.strip())

#             fetch_err = fetch_process.stderr.read()
#             if fetch_err:
#                 self.master.after(0, self.append_output, f"Fetch Errors:\n{fetch_err}")

#             fetch_code = fetch_process.wait()
#             self.master.after(0, self.append_output, f"Tweet fetching completed (code: {fetch_code})")

#             # Guard: only analyze when fetch succeeded OR cached raw_tweets.txt exists
#             if fetch_code != 0 and not os.path.exists(raw_path):
#                 self.master.after(0, self.append_output,
#                                    "No tweets to analyze (fetch failed and no cache). "
#                                     )
#                 return

#             # divider between phases
#             self.master.after(0, self._thick_divider, "End of Fetch — Begin Analysis")

#             # --- Step 2: Analyze Sentiment ---
#             self.master.after(0, self.append_output, "Starting sentiment analysis...")
#             analyze_process = subprocess.Popen(
#                 [sys.executable, analyze_path],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 cwd=SCRIPT_DIR,
#                 env=_subprocess_env(),
#             )

#             for line in analyze_process.stdout:
#                 self.master.after(0, self.append_output, line.strip())

#             analyze_err = analyze_process.stderr.read()
#             if analyze_err:
#                 self.master.after(0, self.append_output, f"Analysis Errors:\n{analyze_err}")

#             analyze_code = analyze_process.wait()
#             self.master.after(0, self.append_output, f"Sentiment analysis completed (code: {analyze_code})")

#             # summary badges like the newer GUI
#             self.master.after(0, self._divider, "Summary")
#             self.master.after(0, self._badge_summary)

#         except Exception as e:
#             self.master.after(0, self.append_output, f"Exception occurred: {e}")

#      # new method to open history viewer           
#     def open_history_viewer(self):
#         # lightweight non-modal “Connecting…” label
#         wait = tk.Toplevel(self.master)
#         wait.title("History")
#         wait.geometry("260x80")
#         wait.transient(self.master)
#         tk.Label(wait, text="Connecting to database…").pack(expand=True, pady=16)

#         def _connect_and_launch():
#             try:
#                 driver = GraphDatabase.driver(URI, auth=AUTH)
#                 driver.verify_connectivity()
#                 self.master.after(0, lambda: (wait.destroy(), HistoryWindow(self.master, driver)))
#             except Exception as e:
#                 self.master.after(0, lambda: (wait.destroy(), tkinter.messagebox.showerror(
#                     "Neo4j Connection Error", f"Could not connect to Neo4j:\n{e}"
#                 )))
#         threading.Thread(target=_connect_and_launch, daemon=True).start()
#     # ===== Output appenders =====
#     def append_output(self, output):
#         """Render lines in a grouped, pretty block (RAW -> CLEANED -> SENTIMENT)."""
#         try:
#             self._pretty_ingest_line(output)
#         except Exception:
#             self.output_text.insert(tk.END, output + '\n')
#             self.output_text.see(tk.END)
#         print(output)

#     def open_fetch_tweets(self):
#         threading.Thread(target=self.run_fetch_tweets).start()

#     def run_fetch_tweets(self):
#         def fetch():
#             keyword = self.keyword_entry.get()
#             if not keyword:
#                 self.master.after(0, self.append_output, "Please enter a movie keyword first.")
#                 return

#             self.master.after(0, self.append_output, "Fetching tweets for sentiment analysis...")

#             script_path = os.path.join(os.path.dirname(__file__), "fetch_tweets.py")
#             try:
#                 process = subprocess.Popen(
#                     [sys.executable, script_path, keyword, CURRENT_USER],
#                     stdout=subprocess.PIPE,
#                     stderr=subprocess.PIPE,
#                     text=True,
#                     cwd=SCRIPT_DIR,
#                     env=_subprocess_env(),
#                 )

#                 for line in process.stdout:
#                     self.master.after(0, self.append_output, line.strip())

#                 errors = process.stderr.read()
#                 if errors:
#                     self.master.after(0, self.append_output, f"Error:\n{errors}")

#                 return_code = process.wait()
#                 self.master.after(0, self.append_output, f"Tweet fetching completed with return code: {return_code}")

#             except Exception as e:
#                 self.master.after(0, self.append_output, f"Exception occurred: {e}")

#         thread = threading.Thread(target=fetch, daemon=True)
#         thread.start()

#     def open_sentiment_analysis(self):
#         threading.Thread(target=self.run_sentiment_analysis).start()

#     def run_sentiment_analysis(self):
#         def analyze():
#             self.master.after(0, self.append_output, "Cleaning tweets and preparing for sentiment analysis...")
#             script_path = os.path.join(os.path.dirname(__file__), "analyze_sentiment.py")

#             try:
#                 process = subprocess.Popen(
#                     [sys.executable, script_path],
#                     stdout=subprocess.PIPE,
#                     stderr=subprocess.PIPE,
#                     text=True,
#                     cwd=SCRIPT_DIR,
#                     env=_subprocess_env(),
#                 )

#                 for line in process.stdout:
#                     self.master.after(0, self.append_output, line.strip())

#                 errors = process.stderr.read()
#                 if errors:
#                     self.master.after(0, self.append_output, f"Error:\n{errors}")

#                 return_code = process.wait()
#                 self.master.after(0, self.append_output, f"Sentiment cleaning completed with return code: {return_code}")

#             except Exception as e:
#                 self.master.after(0, self.append_output, f"Exception occured: {e}")

#         thread = threading.Thread(target=analyze, daemon=True)
#         thread.start()


# # NEW CLASS: HistoryWindow (modern table-style)

# class HistoryWindow(tk.Toplevel):
#     """
#     A searchable history UI for all stored tweets/analyses.
#     Filters: run, keyword, username, date range, sentiment, score, contains text.
#     Pagination + CSV export.
#     """
#     def __init__(self, master, driver):
#         super().__init__(master)
#         self.title("Tweetables — History")
#         self.geometry("1100x1000")
#         self.configure(bg="#F3F4F6")

#         self.limit = 100
#         self.skip = 0

#         # Neo4j connection (already opened by caller)
#         self.driver = driver

#         # ----- Filters -----
#         filt = tk.Frame(self, bg="#F3F4F6")
#         filt.pack(side=tk.TOP, fill=tk.X, padx=12, pady=8)

#         tk.Label(filt, text="Keyword:", bg="#F3F4F6").grid(row=0, column=0, sticky="w")
#         self.keyword_var = tk.StringVar()
#         ttk.Entry(filt, textvariable=self.keyword_var, width=18).grid(row=0, column=1, padx=6)

#         tk.Label(filt, text="Run ID:", bg="#F3F4F6").grid(row=0, column=2, sticky="w")
#         self.run_var = tk.StringVar()
#         self.run_combo = ttk.Combobox(filt, textvariable=self.run_var, width=40)
#         self.run_combo.grid(row=0, column=3, padx=6)

#         tk.Label(filt, text="Username:", bg="#F3F4F6").grid(row=0, column=4, sticky="w")
#         self.user_var = tk.StringVar(value="")
#         ttk.Entry(filt, textvariable=self.user_var, width=18).grid(row=0, column=5, padx=6)

#         tk.Label(filt, text="Date From (YYYY-MM-DD):", bg="#F3F4F6").grid(row=1, column=0, sticky="w")
#         self.date_from_var = tk.StringVar()
#         ttk.Entry(filt, textvariable=self.date_from_var, width=18).grid(row=1, column=1, padx=6)

#         tk.Label(filt, text="Date To (YYYY-MM-DD):", bg="#F3F4F6").grid(row=1, column=2, sticky="w")
#         self.date_to_var = tk.StringVar()
#         ttk.Entry(filt, textvariable=self.date_to_var, width=18).grid(row=1, column=3, padx=6)

#         tk.Label(filt, text="Sentiment:", bg="#F3F4F6").grid(row=2, column=0, sticky="w")
#         self.sentiment_var = tk.StringVar()
#         self.sentiment_combo = ttk.Combobox(
#             filt, textvariable=self.sentiment_var,
#             values=["", "Positive", "Neutral", "Negative"], width=16
#         )
#         self.sentiment_combo.grid(row=2, column=1, padx=6)
#         self.sentiment_combo.current(0)

#         tk.Label(filt, text="Min Score:", bg="#F3F4F6").grid(row=2, column=2, sticky="w")
#         self.min_score_var = tk.StringVar()
#         ttk.Entry(filt, textvariable=self.min_score_var, width=10).grid(row=2, column=3, padx=6, sticky="w")

#         tk.Label(filt, text="Max Score:", bg="#F3F4F6").grid(row=2, column=4, sticky="w")
#         self.max_score_var = tk.StringVar()
#         ttk.Entry(filt, textvariable=self.max_score_var, width=10).grid(row=2, column=5, padx=6, sticky="w")

#         tk.Label(filt, text="Text contains:", bg="#F3F4F6").grid(row=3, column=0, sticky="w")
#         self.contains_var = tk.StringVar()
#         ttk.Entry(filt, textvariable=self.contains_var, width=40)\
#             .grid(row=3, column=1, columnspan=3, padx=6, sticky="we")

#         btns = tk.Frame(filt, bg="#F3F4F6")
#         btns.grid(row=4, column=0, columnspan=6, sticky="w", pady=(8, 4))
#         ttk.Button(btns, text="Search", command=self.search).grid(row=0, column=0, padx=4)
#         ttk.Button(btns, text="Reset", command=self.reset_filters).grid(row=0, column=1, padx=4)
#         ttk.Button(btns, text="Export CSV", command=self.export_csv).grid(row=0, column=2, padx=12)

#         # ----- Results table -----
#         table_frame = tk.Frame(self, bg="#F3F4F6")
#         table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

#         self.tree = ttk.Treeview(
#             table_frame,
#             columns=("created_at","keyword","author_handle","author_name","ingester",
#                      "run_id","sentiment","score","text"),
#             show="headings", height=16
#         )

#         self.tree.heading("created_at", text="Created At")
#         self.tree.heading("keyword", text="Keyword")
#         self.tree.heading("author_handle", text="Author (handle)")
#         self.tree.heading("author_name", text="Author (name)")
#         self.tree.heading("ingester", text="Ingester")
#         self.tree.heading("run_id", text="Run ID")
#         self.tree.heading("sentiment", text="Sentiment")
#         self.tree.heading("score", text="Score")
#         self.tree.heading("text", text="Text")

#         self.tree.column("created_at", width=160, anchor="w")
#         self.tree.column("keyword", width=120, anchor="w")
#         self.tree.column("author_handle", width=150, anchor="w")
#         self.tree.column("author_name", width=180, anchor="w")
#         self.tree.column("ingester", width=120, anchor="w")
#         self.tree.column("run_id", width=260, anchor="w")
#         self.tree.column("sentiment", width=100, anchor="center")
#         self.tree.column("score", width=70, anchor="center")
#         self.tree.column("text", width=800, anchor="w")

#         vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscroll=vsb.set)
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         vsb.pack(side=tk.RIGHT, fill=tk.Y)

#         # ----- Pager -----
#         pager = tk.Frame(self, bg="#F3F4F6")
#         pager.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=8)
#         ttk.Button(pager, text="◀ Prev", command=self.prev_page).pack(side=tk.LEFT)
#         ttk.Button(pager, text="Next ▶", command=self.next_page).pack(side=tk.LEFT, padx=6)
#         self.count_label = tk.Label(pager, text="", bg="#F3F4F6")
#         self.count_label.pack(side=tk.RIGHT)

#         # Preload run list + initial search
#         self._load_runs_into_dropdown()
#         self.search()

#     # ---------- helpers ----------
#     def _load_runs_into_dropdown(self):
#         cy = """
#         MATCH (r:RUN)
#         RETURN r.id AS id, r.keyword AS keyword, r.ts AS ts
#         ORDER BY coalesce(r.ts, datetime()) DESC
#         LIMIT 200
#         """
#         try:
#             recs, _, _ = self.driver.execute_query(cy)
#             opts = [f"{r.get('keyword') or ''} • {r['id']}" for r in recs]
#             self.run_combo["values"] = [""] + opts
#         except Exception as e:
#             messagebox.showerror("Neo4j Error", str(e))

#     def _parse_run_id(self, combo_value: str):
#         if not combo_value:
#             return None
#         if "•" in combo_value:
#             return combo_value.split("•", 1)[1].strip()
#         return combo_value.strip()

#     def _build_params(self):
#         p = {
#             "keyword": self.keyword_var.get().strip() or None,
#             "run_id": self._parse_run_id(self.run_var.get().strip()),
#             "user": self.user_var.get().strip() or None,
#             "date_from": self.date_from_var.get().strip() or None,
#             "date_to": self.date_to_var.get().strip() or None,
#             "sentiment": self.sentiment_var.get().strip() or None,
#             "min_score": None,
#             "max_score": None,
#             "contains": self.contains_var.get().strip().lower() or None,
#             "skip": self.skip,
#             "limit": self.limit,
#         }
#         try:
#             if self.min_score_var.get().strip():
#                 p["min_score"] = float(self.min_score_var.get().strip())
#             if self.max_score_var.get().strip():
#                 p["max_score"] = float(self.max_score_var.get().strip())
#         except ValueError:
#             messagebox.showerror("Input Error", "Min/Max Score must be numbers.")
#         return p

#     def _query_count(self, params):
#         cy = """
#         MATCH (t:Tweet)
#         OPTIONAL MATCH (t)-[:MENTIONS]->(k:Keyword)
#         OPTIONAL MATCH (t)<-[:INGESTED]-(ing:USER)
#         OPTIONAL MATCH (t)-[:BY|:AUTHORED_BY|:CREATED_BY]->(a)
#         OPTIONAL MATCH (t)-[:OF_RUN]->(r:RUN)
#         OPTIONAL MATCH (t)-[:HAS_CLEANED]->(c:CleanedTweet)
#         WITH t,k,ing,a,r,c,
#              toLower(coalesce(t.author_username,a.username,a.handle,a.screen_name,ing.username,'')) AS who,
#              toLower(t.text) AS rawtxt,
#              toLower(coalesce(c.cleaned,'')) AS cleantxt
#         WHERE ($keyword  IS NULL OR toLower(k.name) CONTAINS toLower($keyword))
#           AND ($run_id   IS NULL OR r.id = $run_id)
#           AND ($user     IS NULL OR who CONTAINS toLower($user))
#           AND ($contains IS NULL OR rawtxt CONTAINS $contains OR cleantxt CONTAINS $contains)
#           AND ($date_from IS NULL OR t.created_at >= datetime($date_from))
#           AND ($date_to   IS NULL OR t.created_at <  datetime($date_to) + duration('P1D'))
#           AND ($sentiment IS NULL OR c.sentiment = $sentiment)
#           AND ($min_score IS NULL OR c.score >= $min_score)
#           AND ($max_score IS NULL OR c.score <= $max_score)
#         RETURN count(*) AS n
#         """
#         recs, _, _ = self.driver.execute_query(cy, params)
#         return recs[0]["n"]

#     def _query_page(self, params):
#         cy = """
#         MATCH (t:Tweet)
#         OPTIONAL MATCH (t)-[:MENTIONS]->(k:Keyword)
#         OPTIONAL MATCH (t)<-[:INGESTED]-(ing:USER)
#         OPTIONAL MATCH (t)-[:BY|:AUTHORED_BY|:CREATED_BY]->(a)
#         OPTIONAL MATCH (t)-[:OF_RUN]->(r:RUN)
#         OPTIONAL MATCH (t)-[:HAS_CLEANED]->(c:CleanedTweet)
#         WITH t,k,ing,a,r,c,
#              toLower(coalesce(t.author_username,a.username,a.handle,a.screen_name,ing.username,'')) AS who,
#              toLower(t.text) AS rawtxt,
#              toLower(coalesce(c.cleaned,'')) AS cleantxt
#         WHERE ($keyword  IS NULL OR toLower(k.name) CONTAINS toLower($keyword))
#           AND ($run_id   IS NULL OR r.id = $run_id)
#           AND ($user     IS NULL OR who CONTAINS toLower($user))
#           AND ($contains IS NULL OR rawtxt CONTAINS $contains OR cleantxt CONTAINS $contains)
#           AND ($date_from IS NULL OR t.created_at >= datetime($date_from))
#           AND ($date_to   IS NULL OR t.created_at <  datetime($date_to) + duration('P1D'))
#           AND ($sentiment IS NULL OR c.sentiment = $sentiment)
#           AND ($min_score IS NULL OR c.score >= $min_score)
#           AND ($max_score IS NULL OR c.score <= $max_score)
#         RETURN
#             t.id                AS id,
#             t.created_at        AS created_at,
#             coalesce(k.name,'') AS keyword,
#             coalesce(t.author_username,a.username,a.handle,a.screen_name,'') AS author_handle,
#             coalesce(t.author_name,a.name,'')                                AS author_name,
#             coalesce(ing.username,'')                                        AS ingester,
#             r.id                AS run_id,
#             c.sentiment         AS sentiment,
#             c.score             AS score,
#             t.text              AS text
#         ORDER BY t.created_at DESC
#         SKIP $skip LIMIT $limit
#         """
#         recs, _, _ = self.driver.execute_query(cy, params)
#         rows = []
#         for r in recs:
#             rows.append({
#                 "created_at": str(r.get("created_at") or ""),
#                 "keyword": r.get("keyword") or "",
#                 "author_handle": r.get("author_handle") or "",
#                 "author_name": r.get("author_name") or "",
#                 "ingester": r.get("ingester") or "",
#                 "run_id": r.get("run_id") or "",
#                 "sentiment": r.get("sentiment") or "",
#                 "score": r.get("score"),
#                 "text": r.get("text") or "",
#             })
#         return rows

#     def search(self):
#         try:
#             self.skip = 0
#             params = self._build_params()
#             total = self._query_count(params)
#             self._load_page(params, total)
#         except Exception as e:
#             messagebox.showerror("Neo4j Error", str(e))

#     def _load_page(self, params, total):
#         for i in self.tree.get_children():
#             self.tree.delete(i)
#         rows = self._query_page(params)
#         for row in rows:
#             self.tree.insert("", tk.END, values=(
#                 row["created_at"], row["keyword"], row["author_handle"], row["author_name"],
#                 row["ingester"], row["run_id"], row["sentiment"], row["score"], row["text"]
#             ))
#         start = params["skip"] + 1 if total > 0 else 0
#         end = min(params["skip"] + self.limit, total)
#         self.count_label.config(text=f"Showing {start}-{end} of {total}")

#     def next_page(self):
#         try:
#             params = self._build_params()
#             total = self._query_count(params)
#             if self.skip + self.limit < total:
#                 self.skip += self.limit
#                 params["skip"] = self.skip
#                 self._load_page(params, total)
#         except Exception as e:
#             messagebox.showerror("Neo4j Error", str(e))

#     def prev_page(self):
#         try:
#             if self.skip >= self.limit:
#                 self.skip -= self.limit
#             else:
#                 self.skip = 0
#             params = self._build_params()
#             total = self._query_count(params)
#             params["skip"] = self.skip
#             self._load_page(params, total)
#         except Exception as e:
#             messagebox.showerror("Neo4j Error", str(e))

#     def reset_filters(self):
#         self.keyword_var.set("")
#         self.run_var.set("")
#         self.user_var.set("")
#         self.date_from_var.set("")
#         self.date_to_var.set("")
#         self.sentiment_var.set("")
#         self.min_score_var.set("")
#         self.max_score_var.set("")
#         self.contains_var.set("")
#         self.skip = 0
#         self.search()

#     def export_csv(self):
#         try:
#             params = self._build_params()
#             all_params = dict(params)
#             all_params["skip"] = 0
#             all_params["limit"] = 100000
#             rows = self._query_page(all_params)

#             if not rows:
#                 messagebox.showinfo("Export", "No rows to export for the current filters.")
#                 return

#             path = filedialog.asksaveasfilename(
#                 defaultextension=".csv",
#                 filetypes=[("CSV", "*.csv")],
#                 title="Save history as CSV"
#             )
#             if not path:
#                 return

#             import csv
#             with open(path, "w", newline="", encoding="utf-8") as f:
#                 w = csv.writer(f)
#                 w.writerow(["created_at","keyword","author_handle","author_name","ingester",
#                             "run_id","sentiment","score","text"])
#                 for r in rows:
#                     w.writerow([
#                         r["created_at"], r["keyword"], r["author_handle"], r["author_name"],
#                         r["ingester"], r["run_id"], r["sentiment"], r["score"], r["text"]
#                     ])
#             messagebox.showinfo("Export", f"Saved {len(rows)} rows to {path}")
#         except Exception as e:
#             messagebox.showerror("Export Error", str(e))

#     def destroy(self):
#         # Close the Neo4j driver when the window closes
#         try:
#             self.driver.close()
#         except Exception:
#             pass
#         return super().destroy()


# if __name__ == "__main__":
#     root = tk.Tk()
#     login = LoginScreen(root)
#     root.mainloop()









# New main.py simplfied version:
# main.py
import os
import sys
import tkinter as tk

# (Optional) nicer text rendering on Windows HiDPI
if sys.platform.startswith("win"):
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor v1
    except Exception:
        pass

# Ensure we run from the project root so relative paths (logo, scripts) work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Import after chdir so modules that rely on BASE_DIR/SCRIPT_DIR behave
from widgets.login_screen import LoginScreen  # your new split-out login
# If you put shared constants in settings.py, it will load .env on import

def main():
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()