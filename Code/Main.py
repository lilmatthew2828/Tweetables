
import tkinter as tk
import threading
import subprocess
import os
import sys
import tkinter.messagebox

#USER.TXT IS MASSIVELY IMPORTANT FOR LOGGING IN. 
#MY GOAL IS TOO MAKE SO IT CAN HOLD A NUMBER OF VARIOUS POSSIBLE LOGIN CREDNETIALS TOO MAKE THIS MORE REALISTIC 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.txt")


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
            self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Username or password is wrong", fg="red") # if those crendentials are incorrect
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def check_credentials(self, username, password): # Fixed This as well You hit this because some lines in users.txt have more than one comma, so
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as file:
                for raw in file:
                    line = raw.strip()
                    if not line:
                        continue                      # skip blanks
                    if line.startswith("#"):
                        continue                      # allow comments

                    # split only once: username , password-with-commas-allowed
                    parts = line.split(",", 1)
                    if len(parts) < 2:
                        continue                      # skip malformed lines

                    stored_user = parts[0].strip()
                    stored_pass = parts[1].strip()

                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "No users found. Please Sign Up first.")
            return False
        return False

    def open_signup(self): #method for user sign up process. Needs ode tweaking 
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("350x200")
        signup_window.configure(bg="#ADD8E6")

        frame = tk.Frame(signup_window, bg="#ADD8E6", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="New Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        new_username = tk.Entry(frame, font=("Arial", 12))
        new_username.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="New Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
        new_password = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password.grid(row=1, column=1, pady=5, padx=10)
#=================================================================================================================================================================================================
        def save_credentials():
            username = new_username.get().strip()
            password = new_password.get().strip()

            # Basic validation
            if not username or not password:
                tk.messagebox.showerror("Error", "Username and password are required.")
                return
            if "," in username or "," in password:
                tk.messagebox.showerror("Error", "Commas are not allowed in username or password.")
                return

            try:
                # 1) Ensure the file exists
                if not os.path.exists(USERS_FILE):
                    with open(USERS_FILE, "w", encoding="utf-8"):
                        pass

                # 2) Check duplicates safely (skip malformed/blank lines)
                existing = set()
                with open(USERS_FILE, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(",")
                        if len(parts) < 2:
                            continue
                        stored_user = parts[0]
                        existing.add(stored_user)

                if username in existing:
                    tk.messagebox.showerror("Error", "Username already exists.")
                    return

                # 3) Append the new user (this was previously inside the except!)
                with open(USERS_FILE, "a", encoding="utf-8") as file:
                    file.write(f"{username},{password}\n")

                tk.messagebox.showinfo("Success", "Account created. You can log in now.")
                signup_window.destroy()

            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not save credentials:\n{e}")

        signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        signup_button.grid(row=2, columnspan=2, pady=10)
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
        self.master.geometry("600x450")
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
        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.search_button.grid(row=0, column=0, padx=5)
        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.analysis_button.grid(row=0, column=1, padx=5)
    
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
                    [sys.executable, script_path, keyword], #pass keyword here 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True
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
                    text=True
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