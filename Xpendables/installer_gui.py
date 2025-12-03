"""
Tweetables GUI Installer
Created by: Xpendables Team (Day's design, cleaned & wired up)

- Cross-platform: Windows + macOS
- Creates/uses a Python virtual environment (venv)
- Installs requirements from requirements.txt
- Verifies .env exists
- Launches Main.py inside the venv
"""

import os
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# ---------- Paths & helpers ----------

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)  # make sure we run from project root


def run_cmd(cmd: str) -> int:
    """Run a shell command and return its exit code."""
    # shell=True lets us pass the command string like in your pseudocode
    completed = subprocess.run(cmd, shell=True)
    return completed.returncode


def update_progress(progress_widget, percent_label, step, total_steps, status_label=None, msg=None):
    """Update progress bar + % label (and optional status text)."""
    if msg is not None and status_label is not None:
        status_label.config(text=msg)

    percent = int((step / total_steps) * 100)
    progress_widget["value"] = percent
    percent_label.config(text=f"{percent}%")
    app.update_idletasks()


# ---------- macOS installer ----------

def install_mac(progress, status_label, percent_label):
    steps = [
        ("Checking for existing virtual environment...", None),
        ("Creating virtual environment...", "python3 -m venv venv"),
        ("Activating virtual environment...", "source venv/bin/activate"),
        ("Upgrading pip...", "venv/bin/python3 -m pip install --upgrade pip"),
        ("Installing dependencies...", "venv/bin/python3 -m pip install -r requirements.txt"),
        ("Checking .env file...", None),
        ("Launching Tweetables...", "venv/bin/python3 Main.py"),
    ]
    total_steps = len(steps)

    for i, (msg, cmd) in enumerate(steps, start=1):
        # Step: check for existing venv
        if msg.startswith("Checking for existing virtual environment"):
            update_progress(progress, percent_label, i, total_steps, status_label, msg)
            if (BASE_DIR / "venv").is_dir():
                status_label.config(
                    text="Virtual environment detected. Skipping recreation..."
                )
            continue

        # Step: check .env
        if msg.startswith("Checking .env file"):
            update_progress(progress, percent_label, i, total_steps, status_label, msg)
            env_path = BASE_DIR / ".env"
            if not env_path.is_file():
                messagebox.showerror(
                    "Error", ".env file is missing. Please add it and re-run installer."
                )
                return
            continue

        # Normal command step
        update_progress(progress, percent_label, i, total_steps, status_label, msg)

        if cmd:
            code = run_cmd(cmd)
            if code != 0:
                messagebox.showerror(
                    "Installation error",
                    f"Command failed:\n{cmd}\n\nExit code: {code}",
                )
                return

    messagebox.showinfo("Success", "Tweetables successfully installed. Launching app...")
    status_label.config(text="Installation complete.")


# ---------- Windows installer ----------

def install_windows(progress, status_label, percent_label):
    # NOTE: we directly call venv\Scripts\python and venv\Scripts\pip
    # so we don't rely on 'activate' changing this process's environment.
    steps = [
        ("Checking for existing virtual environment...", None),
        ("Creating virtual environment...", "python -m venv venv"),
        ("Activating virtual environment...", "call venv\\Scripts\\activate"),
        # ★ use python -m pip instead of pip directly
        ("Upgrading pip...", "venv\\Scripts\\python.exe -m pip install --upgrade pip"),
        ("Installing dependencies...", "venv\\Scripts\\python.exe -m pip install -r requirements.txt"),
        ("Checking .env file...", None),
        ("Launching Tweetables...", "venv\\Scripts\\python.exe Main.py"),
    ]

    total_steps = len(steps)

    for i, (msg, cmd) in enumerate(steps, start=1):
        # Step: check for existing venv
        if msg.startswith("Checking for existing virtual environment"):
            update_progress(progress, percent_label, i, total_steps, status_label, msg)
            # Check for Scripts\python as a good indicator
            if (BASE_DIR / "venv" / "Scripts" / "python.exe").is_file():
                status_label.config(
                    text="Virtual environment detected. Skipping recreation..."
                )
            continue

        # Step: check .env
        if msg.startswith("Checking .env file"):
            update_progress(progress, percent_label, i, total_steps, status_label, msg)
            env_path = BASE_DIR / ".env"
            if not env_path.is_file():
                messagebox.showerror(
                    "Error", ".env file is missing. Please add it and re-run installer."
                )
                return
            continue

        # Normal command step
        update_progress(progress, percent_label, i, total_steps, status_label, msg)

        if cmd:
            code = run_cmd(cmd)
            if code != 0:
                messagebox.showerror(
                    "Installation error",
                    f"Command failed:\n{cmd}\n\nExit code: {code}",
                )
                return

    messagebox.showinfo("Success", "Tweetables successfully installed. Launching app...")
    status_label.config(text="Installation complete.")


# ---------- OS selection / threading ----------

def run_install():
    """Detect OS and run the appropriate installer (in background thread)."""
    os_name = platform.system()

    if os_name == "Darwin":  # macOS
        install_mac(progress, status_label, percent_label)
    elif os_name == "Windows":
        install_windows(progress, status_label, percent_label)
    else:
        messagebox.showerror(
            "OS not supported",
            "This installer only supports macOS or Windows.",
        )

    # Re-enable button after we’re done (success or error)
    install_button.config(state="normal")


def start_install():
    """Start installation when user clicks the button."""
    install_button.config(state="disabled")
    status_label.config(text="Starting installation...")

    thread = threading.Thread(target=run_install, daemon=True)
    thread.start()


# ---------- GUI ----------

app = tk.Tk()
app.title("Tweetables Installer")
app.geometry("880x860")
app.configure(bg="black")
app.resizable(False, False)

# Logo section
from pathlib import Path
from PIL import Image, ImageTk   # only if you're not already importing these

# --- Logo frame ---
logo_frame = tk.Frame(app, bg="black")
logo_frame.pack(pady=20)

# Use *project-relative* path instead of a hard-coded absolute Windows path
BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "Xpendables.png"   # put Xpendables.png in same folder as installer_gui.py

if logo_path.exists():
    try:
        # Load + resize (tweak 160x160 to whatever looks best)
        img = Image.open(logo_path)
        img = img.resize((160, 160))          # <--- smaller logo size
        logo_img = ImageTk.PhotoImage(img)

        logo_label = tk.Label(logo_frame, image=logo_img, bg="black")
        logo_label.pack()
        # keep reference so image doesn't disappear
        app.logo_img_ref = logo_img
    except Exception as e:
        tk.Label(
            logo_frame,
            text="[Logo failed to load]",
            fg="white",
            bg="black",
            font=("Arial", 14, "italic")
        ).pack(pady=10)
else:
    tk.Label(
        logo_frame,
        text="[Logo missing]",
        fg="white",
        bg="black",
        font=("Arial", 14, "italic")
    ).pack(pady=10)

# Title
tk.Label(
    app,
    text="Tweetables Installer",
    fg="white",
    bg="black",
    font=("Arial", 16, "bold"),
).pack(pady=(0, 10))

# Status label
status_label = tk.Label(
    app,
    text="Ready to install Tweetables.",
    fg="white",
    bg="black",
    font=("Arial", 11),
)
status_label.pack(pady=(5, 15))

# Progress bar + percentage
progress_frame = tk.Frame(app, bg="black")
progress_frame.pack(pady=10)

progress = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    mode="determinate",
    length=260
)
progress.pack(anchor="center")

percent_label = tk.Label(
    progress_frame,
    text="0%",
    fg="white",
    bg="black",
    font=("Arial", 10)
)
percent_label.pack(anchor="center", pady=5)

# Install button
install_button = tk.Button(
    app,
    text="Install / Launch Tweetables",
    command=start_install,
    fg="black",
    bg="white",
    font=("Arial", 12, "bold"),
    padx=12,
    pady=8,
)
install_button.pack(pady=30)

# Footer hint
tk.Label(
    app,
    text="Python 3.10+ and internet required on first run.",
    fg="gray",
    bg="black",
    font=("Arial", 9),
).pack(side="bottom", pady=10)

if __name__ == "__main__":
    app.mainloop()
