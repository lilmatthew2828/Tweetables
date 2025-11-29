"""
Tweetables upgraded GUI Installer from the installtion scripts 
Created by: Day Ekoi

Purpose: this GUI replaces the orginial macOS & Windows instalation scripts created and presented in iteration 4.
It now provides a unified, cross platform instalation GUI. 
Previously the installation scripts (install_mac.command & install_windows.bat):
- Created, avtivated, and maanaged the python Virtual Environment (venv)
- Instaled all dependecies from the requirements.txt fule
- Validation of .env file
- Launched application after full installation
- Displayed messages informing user on the current steps

The upgrades in this version now:
- Incorporate Dark-Mode themed GUI to go hand in hand without our teams colors 
- Has our Team logo
- Has a progress bar to track installation
- Removes the terminal interaction required on macOS
"""

import os 
import platform                          # Detects macOS or Windows
import subprocess                        # Runs terminal/command line commands
import threading                         # runs installation without any freezes of the GUI
import tkinter as tk                     # Pythons GUI framework
from tkinter import ttk, messagebox 
import pathlib import Path               # checks for file existence such as the logo

# Running of OS Commands
def run_cmd(cmd):                        # runs shell command as it would in Terminal/Compand Prompt
  return subprocess.run(cmd, shell=True) # True allows for string based commands

# Progress Bar
def update_progress(progress_widget, percent_label, step, total_steps): # updates progress bar and percentage 
  percent = int((step / total_steps) * 100) # Calculate percentage
  progress_widget["value"] = percent        # Update bar fill amount
  percent_label.config(text=f"{percent}%")  # Show numeric %
  app.update_idletasks()                    # Forces GUI refresh during install

# MacOS Installation 

def install_mac(progress, status_label, percent_label)

  # Installation Steps Messages 

  steps = [
      ("Checking for existing virtual environment...", None),
      ("Creating virtual environment...", "python3 -m venv venv"),
      ("Activating virtual environment...", "source venv/bin/activate"),
      ("Upgrading pip...", "venv/bin/pip install --upgrade pip"),
      ("Installing dependencies...", "venv/bin/pip install -r requirements.txt"),
      ("Checking .env file...", None),
      ("Launching Tweetables...", "venv/bin/python3 Main.py")
  ]

toal_steps = len(steps) # Calculates Percentages

# for loop that loops through each step 

for i, (msg, cmd) in enumerate(steps, start=1):
  status_label.config(text=msg) # Updates status 

# Verification to check if venv file exists, this is for when needing to open application again, it doesnt reinstall
  if msg.startswith("Checking for exisiting file"):
    if os.path.isdir("venv"):
      status_label.config(text="Virtual environment detected. Skipping reinstallation and recreation...")
      update_progress(progress, percent_label, i, total_steps)
      continue # skips it

# Checks if there is a .env file
if msg.startswith("Checking for .env file"):
  if not os.path.isfile(".env"):
    messagebox.showerror("Error", ".env file is missing.")
    return # steps the installer because there is no .env file 

# Moves on and runs shell command if it does exist 
if cmd: 
  run_cmd(cmd)

# Update of progress bar
update_progress(progress, percent_label, i, total_steps)

# Success message when installed 
messagebox.showinfo("Tweetables successfuly installed. App Launching...)
status_label.config(text="Installation Complete.")


# Windows Installation

def install_windows(progress, status_label, percent_label)

  # Installation Steps Messages 

  steps = [
      ("Checking for existing virtual environment...", None),
      ("Creating virtual environment...", "python3 -m venv venv"),
      ("Activating virtual environment...", "call venv\\Scripts\\activate"),
      ("Upgrading pip...", "venv\\Scripts\\pip install --upgrade pip"),
      ("Installing dependencies...", "venv\\Scripts\\pip install -r requirements.txt"),
      ("Checking .env file...", None),
      ("Launching Tweetables...", "venv\\Scripts\\python3 Main.py")
  ]

toal_steps = len(steps) # Calculates Percentages

# for loop that loops through each step 

for i, (msg, cmd) in enumerate(steps, start=1):
  status_label.config(text=msg) # Updates status 

# Verification to check if venv file exists, this is for when needing to open application again, it doesnt reinstall
  if msg.startswith("Checking for exisiting file"):
    if os.path.isfile("venv\\Scripts\\activate"):
      status_label.config(text="Virtual environment detected. Skipping reinstallation and recreation...")
      update_progress(progress, percent_label, i, total_steps)
      continue # skips it

# Checks if there is a .env file
if msg.startswith("Checking for .env file"):
  if not os.path.isfile(".env"):
    messagebox.showerror("Error", ".env file is missing.")
    return # steps the installer because there is no .env file 

# Moves on and runs shell command if it does exist 
if cmd: 
  run_cmd(cmd)

# Update of progress bar
  update_progress(progress, percent_label, i, total_steps)

messagebox.showinfo("Tweetables successfully installed. App launching...)
status_label.config(text="Installation complete.")

# Start Installation Function
# This is triggered when user double clicks Install button
def start_install();
  install_button.config(state="disabled")
  status_label.config(text= Starting Installation...")

# Run installler in background to avoid GUI freezing
thread = threading.Thread(target=run_install)
thread.start()

def run_install(); #Detects OS and chooses correct installer
os_name = platform.system()

if os_name == "Darwin": # Darwin is macOS
  install_mac(progress, status_label, percent_label)
elif os_name == "Windows":
  install_windows(progress, status_label, percent_label)
else:
  messagebox.showerror("OS not supported", "This installer only supports macOS or Windows.")
  
  install_button.config(state="normal")


# GUI Theme

app = tk.TK()
app.title("Tweetables Installer")
app.geometry("430x560")
app.configure(bg="black")
app.resizable(False, False)

# Logo

logo_frame = tk.Frame(app, bg="black")
logo_frame.pack(pady=20)

if Path("Xpendables.png").exists():
  logo_img = tk.PhotoImage(file="Xpendables.png")
  tk.Label(logo_frame, image=logo_img, bg="black").pack()
else
  tk.Label(app, text="Xpendables missing]",
           fg="white", bg="black",
           font=("Arial", 14, "italic")).pack(pady=10)
                  



                    


                    
                    


            
                    



  
                
  
