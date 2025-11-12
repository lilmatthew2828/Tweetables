@echo off
REM run_app.bat: Tweetables Windows Launcher
REM Purpose: Launches application on macOS by creating VE, installing all packages, and running automatically
REM Creator: Day Ekoi

echo _________________________
echo Launching Tweetables 
echo _________________________


REM Step 1: Verify VE exists

    if not exist "venv\Scripts\activate" (
        echo Virtual Environement not found.
        echo Please run install_windows.bat first
        pause
        exit /b
    )

REM Step 2: Activate VE created during install

    call venv\Scripts\activate

REM Step 3: Verify .env file exits 

    if not exist ".env" (
        echo No .env file found
        echo Make sure the .env file exists in the folder before launching.
        pause
        exit /b
    )

REM Step 4: Launch Application

    python Main.py

REM Step 5: Keeps window oopen so user can view output

    echo.
    pause

