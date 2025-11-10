REM run_app.bat: Tweetables Windows Launcher
REM Purpose: Installs and launches application on macOS by creating VE, installing all packages, and running automatically
REM Creator: Day Ekoi

@echo off

REM Step 1: Activate VE created during install

    call venv\Scripts\activate

REM Step 2: Launch Application

    python Main.py

REM Step 3: Keep window oopen so user can view output

    pause

