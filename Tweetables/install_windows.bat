REM Tweetables Windows Installer 
REM Purpose: Creates virtual environement, installs required Python packes, and lauches the app with a double click
REM Creator: Day Ekoi 

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

REM Step 4: Verification of .env file

    if not exist ".env" 
    (    echo No .env file found
         echo Make sure the .env file exists in the folder before launching.
         pause
         exit /b
    )

REM Step 5: Installation Complete 

    echo Installation Complete.
    echo Launching Tweetables...
    python Main.py

    pause
