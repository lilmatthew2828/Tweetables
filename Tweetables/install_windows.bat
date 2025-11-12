@echo off

REM Makes sure it tracks which ever directory the Tweetables folder is in
cd /d "%~dp0"  

REM Tweetables Windows Installer 
REM Purpose: Creates virtual environement, installs required Python packes, and lauches the app with a double click
REM Creator: Day Ekoi 

    echo ____________________________________
    echo Tweetables Installer (Windows)
    echo ____________________________________


REM Step 0: Check if venv already exists

    if exist "venv\Scripts\activate" (
        echo Virtual Environment already exists.
        echo Skipping reinstallation...
        call venv\Scripts\activate
    if not exist ".env" (
        echo No .env file found.
        echo Make sure the .env file exists in the folder before launching.
        pause
        exit /b
    )

    echo Launching Tweetables...
    python Main.py
    echo.
    echo Tweetables has finished running.
    pause
    exit /b
)

REM Step 1: Creating virtual environment 'venv'
REM Keeps installed scripts isolated from system Python

    echo Please Wait, Creating Virtual Environment...
    python -m venv venv

REM Step 2: Activation of Virtual Environment
REM 'call' required for Windows batch files to activate correctly

    echo Activating Virtual Environment...
    call venv\Scripts\activate

REM Step 3: Install Project Dependencies

    echo Installing Required Packages...
    pip install --upgrade pip
    pip install -r requirements.txt

REM Step 4: Verification of .env file

    if not exist ".env" (    
         echo No .env file found
         echo Make sure the .env file exists in the folder before launching.
         pause
         exit /b
    )

REM Step 5: Installation Complete - Auto launch

    echo Installation Complete.
    echo Launching Tweetables...
    python Main.py

    echo.
    pause
