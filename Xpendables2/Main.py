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