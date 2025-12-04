REM Tweetables Windows Installer 
REM Purpose: Creates virtual environement, installs required Python packes, and lauches the app with a double click
REM Creator: Day Ekoi Fall 25'


  @echo off
  cd /d "%~dp0"

REM _____________________________________________________
REM 
REM    echo ____________________________________
REM    echo Tweetables Installer (Windows Only)
REM    echo ____________________________________

REM Step 1: Creating virtual environment 'venv'
REM Keeps installed scripts isolated from system Python

REM   echo Please Wait, Creating Virtual Environment...
REM   python -m venv venv

REM Step 2: Activation of Virtual Environment
REM 'call' required for Windows batch files to activate correctly

REM    echo Activating Virtual Environment...
REM    call venv\Scripts\activate

REM Step 3: Install Project Dependencies

REM    echo Installing Required Packages...
REM    pip install --upgrade pip
REM    pip install -r requirements.txt

REM Step 4: Installation Complete Twetables App is able to be launched (Main.py is the entry point)

REM    echo Installation Complete.
REM    echo Launching Tweetables...
REM    python Main.py

REM Step 5: Slight pause/delay so the command window doesnt immediately close and lets user read any output.
REM   pause
