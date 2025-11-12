#!/bin/bash


#install_mac.command: Tweetables Mac Installer 
#Purpose: Installs and launches application on macOS by creating VE, installing all packages, and running automatically
#Creator: Day Ekoi


#Step 1: Create a VE called 'venv'

    echo "Please Wait, Creating Virtual Environment..."
    python3 -m venv venv

#Step 2: Activate the VE

    echo "Activating Virtual Environment..."
    source venv/bin/activate

#Step 3: Install dependencies from requirements.txt

    echo "Installing required Python packages..."
    pip install --upgrade pip
    pip install -r requirements.txt

#Step 4: Verification of .env file

    if [ ! -f ".env" ];
        then
        echo "No .env file found."
        echo "Make sure the .env file exists in folder before launching"
        exit 1
    fi


#Step 4: Installation complete and launching app

    echo "Installation complete."
    echo "Launching Tweetables..."
    python3 Main.py
