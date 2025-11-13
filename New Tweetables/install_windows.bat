REM Tweetables Windows Installer 
REM Purpose: Creates virtual environement, installs required Python packes, and lauches the app with a double click
REM Creator: Day Ekoi Fall 25'

    @echo off
    echo ____________________________________
    echo Tweetables Installer (Windows Only)
    echo ____________________________________

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

REM Step 4: Installation Complete Twetables App is able to be launched (Main.py is the entry point)

    echo Installation Complete.
    echo Launching Tweetables...
    python Main.py

REM Step 5: Slight pause/delay so the command window doesnt immediately close and lets user read any output.
    pause
