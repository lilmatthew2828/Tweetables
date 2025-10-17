
import tkinter as tk
import threading
import subprocess
import os
import sys
import tkinter.messagebox
from neo4j import GraphDatabase
import tweepy
import bcrypt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

#USER.TXT IS MASSIVELY IMPORTANT FOR LOGGING IN. 
#MY GOAL IS TOO MAKE SO IT CAN HOLD A NUMBER OF VARIOUS POSSIBLE LOGIN CREDNETIALS TOO MAKE THIS MORE REALISTIC 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.txt")
# Make subprocess I/O deterministic across macOS/Windows/VS Code
SCRIPT_DIR = BASE_DIR  # folder containing this Main.py and the other scripts
NLTK_DIR = os.path.join(SCRIPT_DIR, "nltk_data")
os.makedirs(NLTK_DIR, exist_ok=True)

#We will evenutally need to remove this and like save it somewhere safe but these are here for now
URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

CURRENT_USER = None

def _subprocess_env():
    # Add NLTK_DATA so both child scripts find/download data in-project
    env = {**os.environ, "NLTK_DATA": NLTK_DIR}
    # Optional: force scraping fallback so you always have raw_tweets.txt when API 429 happens
    # env["USE_SNSCRAPE"] = "1"
    return env


class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Screen") #Change to login screen
        self.master.geometry("550x650") # size of the login screen gui 
        self.master.configure(bg="#00BFFF") # background color young nigga
 
        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20) 
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        self.message_label = tk.Label(self.frame, text="", fg="red", bg="#ADD8E6", font=("Arial", 10))
        self.message_label.grid(row=2, columnspan=2, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.validate_login, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.login_button.grid(row=3, columnspan=2, pady=10)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.signup_button.grid(row=4, columnspan=2, pady=10)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.check_credentials(username, password):
            self.message_label.config(text="Login successful!", fg="green") #if the login credentials are correct
            CURRENT_USER = username
            self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Username or password is wrong", fg="red") # if those crendentials are incorrect
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def check_credentials(self, username, password): # Fixed This as well You hit this because some lines in users.txt have more than one comma, so
        
        passwordBytes = password.encode('utf-8')

        def check_credentials2(driver, username):
            query = """
                MATCH (u:USER {username: $username})
                RETURN u.hashed_password AS user_password
            """
            records, summary, key = driver.execute_query(query, username=username)
            return bcrypt.checkpw(passwordBytes, records[0]["user_password"])
                        
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            value = check_credentials2(driver, username)
            driver.close()

        return value


    def open_signup(self): #method for user sign up process. Needs ode tweaking 
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("450x450")
        signup_window.configure(bg="#ADD8E6")

        frame = tk.Frame(signup_window, bg="#ADD8E6", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="New Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        new_username = tk.Entry(frame, font=("Arial", 12))
        new_username.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="New Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
        new_password = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(frame, text="Re-enter New Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=2, column=0, sticky="w", pady=5)
        new_password_again = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password_again.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(frame, text="Enter API Key:", font=("Arial", 12), bg="#ADD8E6").grid(row=3, column=0, sticky="w", pady=5)
        new_api_key = tk.Entry(frame, font=("Arial", 12), show="*")
        new_api_key.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(frame, text="Enter API Secret:", font=("Arial", 12), bg="#ADD8E6").grid(row=4, column=0, sticky="w", pady=5)
        new_api_secret = tk.Entry(frame, font=("Arial", 12), show="*")
        new_api_secret.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(frame, text="Enter Access Token:", font=("Arial", 12), bg="#ADD8E6").grid(row=5, column=0, sticky="w", pady=5)
        new_access_token = tk.Entry(frame, font=("Arial", 12), show="*")
        new_access_token.grid(row=5, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Enter Access Secret:", font=("Arial", 12), bg="#ADD8E6").grid(row=6, column=0, sticky="w", pady=5)
        new_access_secret = tk.Entry(frame, font=("Arial", 12), show="*")
        new_access_secret.grid(row=6, column=1, pady=5, padx=10)

        tk.Label(frame, text="Enter Bearer Token:", font=("Arial", 12), bg="#ADD8E6").grid(row=7, column=0, sticky="w", pady=5)
        new_bearer_token = tk.Entry(frame, font=("Arial", 12), show="*")
        new_bearer_token.grid(row=7, column=1, pady=5, padx=10)

#=================================================================================================================================================================================================
        def save_credentials():
            username = new_username.get()
            password = new_password.get()

            # Basic validation
            if not username or not password:
                tk.messagebox.showerror("Error", "Username and password are required.")
                return
            if "," in username or "," in password:
                tk.messagebox.showerror("Error", "Commas are not allowed in username or password.")
                return
            
            # Fucntion to check if username already exists in the database
            def check_exists(driver, username):
                query = """
                    MATCH (u:USER {username: $username})
                    RETURN COUNT(u) AS user_count
                    """
                records, summary, key = driver.execute_query(query, username=username)
                existing = records[0]["user_count"]
                if existing == 0:
                    return False
                else:
                    return True
            
            # Execute the query to check for existing username
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                if check_exists(driver, username):
                    tk.messagebox.showerror("Error", "Username already exists.")
                    return
                driver.close()
            
            # Check if passwords match
            if password != new_password_again.get():
                tk.messagebox.showerror("Error", "Passwords do not match.")
                return
            
            api_key = new_api_key.get()
            api_secret = new_api_secret.get()
            access_token = new_access_token.get()
            access_secret = new_access_secret.get()
            bearer_token = new_bearer_token.get()

            # Validate Twitter API credentials
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True)

            try:
                api.verify_credentials()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Twitter API authentication failed: {e}")
                return
            
            # Encrypt password before saving with one-way bcrypt hashing
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt)

            # Encrypt all API credentials before saving with two-way Fernet encryption
            key = os.getenv("MASTER_KEY")
            f = Fernet(key)
            enc_api_key = f.encrypt(api_key.encode())
            enc_api_secret = f.encrypt(api_secret.encode())
            enc_access_token = f.encrypt(access_token.encode())
            enc_access_secret = f.encrypt(access_secret.encode())
            enc_bearer_token = f.encrypt(bearer_token.encode())

            # Create the function to add new user to the database
            def create_account(driver, username, hashed_password, enc_api_key, enc_api_secret, enc_access_token, enc_access_secret, enc_bearer_token):
                query = """
                    CREATE (u:USER {username: $username, hashed_password: $hashed_password, enc_api_key: $enc_api_key, enc_api_secret: $enc_api_secret, enc_access_token: $enc_access_token, enc_access_secret: $enc_access_secret, enc_bearer_token: $enc_bearer_token})
                    WITH u
                    MATCH (y:USERS) 
                    MERGE (u)-[:IS_A]->(y)
                """
                driver.execute_query(query, username=username, hashed_password=hashed_password, enc_api_key=enc_api_key, enc_api_secret=enc_api_secret, enc_access_token=enc_access_token, enc_access_secret=enc_access_secret, enc_bearer_token=enc_bearer_token)
            
            # Run the function to create the account
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                create_account(driver, username, hashed_password, enc_api_key, enc_api_secret, enc_access_token, enc_access_secret, enc_bearer_token)
                driver.close()

            tk.messagebox.showinfo("Success", "Account created. You can log in now.")
            signup_window.destroy()


        signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        signup_button.grid(row=8, columnspan=2, pady=10)
#=================================================================================================================================================================================================

    def open_sentiment_analysis(self):
        self.master.destroy()
        root = tk.Tk()
        app = SentimentAnalysisApp(root)
        root.mainloop()

class SentimentAnalysisApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Tweetables: Sentiment Analysis")
        self.master.geometry("700x750")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Tweetables: Movie Sentiment Analysis Tool", font=("Helvetica", 16, "bold"), bg="#ADD8E6").pack(pady=10)
        
        # --- keyword entry box ---
        keyword_frame = tk.Frame(self.frame, bg="#ADD8E6")
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # --- output text box with scrollbar ---
        text_frame = tk.Frame(self.frame)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Arial", 12), yscrollcommand=scrollbar.set)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        # --- buttons ---
        btn_frame = tk.Frame(self.frame, bg="#ADD8E6")
        btn_frame.pack(pady=10)

        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets,
                                    font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.search_button.grid(row=0, column=0, padx=5)

        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis,
                                        font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.analysis_button.grid(row=0, column=1, padx=5)

        # separate row for full run, same frame is fine:
        self.full_run_button = tk.Button(
            btn_frame,
            text="Run Full Analysis",
            command=self.run_full_pipeline,
            font=("Arial", 12), bg="white", fg="black", padx=10, pady=5
        )
        self.full_run_button.grid(row=1, column=0, columnspan=2, pady=8)
#=============#=============#=============#=============#=============#=============#=============#=============


    def run_full_pipeline(self):
        threading.Thread(target=self._run_pipeline_thread, daemon=True).start()

    def _run_pipeline_thread(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            self.master.after(0, self.append_output, "Please enter a movie keyword first.")
            return

        fetch_path = os.path.join(SCRIPT_DIR, "fetch_tweets.py")
        analyze_path = os.path.join(SCRIPT_DIR, "analyze_sentiment.py")
        raw_path = os.path.join(SCRIPT_DIR, "raw_tweets.txt")

        try:
            # --- Step 1: Fetch Tweets ---
            self.master.after(0, self.append_output, f"Fetching tweets for '{keyword}'...")
            fetch_process = subprocess.Popen(
                [sys.executable, fetch_path, keyword],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=SCRIPT_DIR,           # ensure consistent read/write folder
                env=_subprocess_env(),    # pass NLTK_DATA / USE_SNSCRAPE, etc.
            )

            for line in fetch_process.stdout:
                self.master.after(0, self.append_output, line.strip())

            fetch_err = fetch_process.stderr.read()
            if fetch_err:
                self.master.after(0, self.append_output, f"Fetch Errors:\n{fetch_err}")

            fetch_code = fetch_process.wait()
            self.master.after(0, self.append_output, f"Tweet fetching completed (code: {fetch_code})")

            # Guard: only analyze when fetch succeeded OR cached raw_tweets.txt exists
            if fetch_code != 0 and not os.path.exists(raw_path):
                self.master.after(0, self.append_output,
                    "No tweets to analyze (fetch failed and no cache). "
                    "Enable fallback scraping with --scrape or set USE_SNSCRAPE=1."
                )
                return

            # --- Step 2: Analyze Sentiment ---
            self.master.after(0, self.append_output, "Starting sentiment analysis...")
            analyze_process = subprocess.Popen(
                [sys.executable, analyze_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=SCRIPT_DIR,
                env=_subprocess_env(),
            )

            for line in analyze_process.stdout:
                self.master.after(0, self.append_output, line.strip())

            analyze_err = analyze_process.stderr.read()
            if analyze_err:
                self.master.after(0, self.append_output, f"Analysis Errors:\n{analyze_err}")

            analyze_code = analyze_process.wait()
            self.master.after(0, self.append_output, f"Sentiment analysis completed (code: {analyze_code})")

        except Exception as e:
            self.master.after(0, self.append_output, f"Exception occurred: {e}")


    def append_output(self, output):
        self.output_text.insert(tk.END, output + '\n')
        self.output_text.see(tk.END)
        print(output)

    def open_fetch_tweets(self):
        threading.Thread(target=self.run_fetch_tweets).start()

    def run_fetch_tweets(self):

        def fetch():
            keyword = self.keyword_entry.get() # get the keyword entered by the user
            
            self.master.after(0, self.append_output, "Fetching tweets for sentiment analysis...")
        
            script_path = os.path.join(os.path.dirname(__file__), "fetch_tweets.py")
            try:
                #pass the keyword as an argument to the script
                process = subprocess.Popen(
                    [sys.executable, script_path, keyword],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=SCRIPT_DIR,
                    env=_subprocess_env(),
                )


                #read output line by line 
                for line in process.stdout:
                    self.master.after(0, self.append_output, line.strip())

                #Capture errors and display them in GUI
                errors = process.stderr.read()
                if errors:
                    self.master.after(0, self.append_output, f"Error:\n{errors}")

                return_code = process.wait()
                self.master.after(0, self.append_output, f"Tweet fetching completed with return code: {return_code}")
                                
            except Exception as e:
                self.master.after(0, self.append_output, f"Exception occurred: {e}")
    
        #run 'fetch' in a new thread
        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

    def open_sentiment_analysis(self):
        threading.Thread(target=self.run_sentiment_analysis).start()

    def run_sentiment_analysis(self):
        
        def analyze():
            self.master.after(0, self.append_output, "Cleaning tweets and preparing for sentiment analysis...")
            script_path = os.path.join(os.path.dirname(__file__), "analyze_sentiment.py")

            try:
                process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=SCRIPT_DIR,
                env=_subprocess_env(),
            )

                for line in process.stdout:
                    self.master.after(0, self.append_output, line.strip())

                errors = process.stderr.read()
                if errors:
                    self.master.after(0, self.append_output, f"Error:\n{errors}")
                
                return_code = process.wait()
                self.master.after(0, self.append_output, f"Sentiment cleaning completed with return code: {return_code}")
            
            except Exception as e:
                self.master.after(0, self.append_output, f"Exception occured: {e}")

        # Run the cleaning script in a new thread so GUI doesn't freeze
        thread = threading.Thread(target=analyze, daemon=True)
        thread.start()









if __name__ == "__main__":
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()