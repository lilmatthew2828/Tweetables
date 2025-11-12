#!/bin/bash
cd "$(dirname "$0")"

#install_mac.command: Tweetables Mac Installer 
#Purpose: Installs and launches application on macOS by creating VE, installing all packages, and running automatically
#Creator: Day Ekoi

echo "____________________________"
echo "Tweetables Installer (macOS)"
echo "____________________________"

#Step 0: Check if VE exists 

    if [ -d "venv" ]; then
        echo "Virtual environment already exists."
        echo "Skipping reinstallation..."

    # Verify that .env exists

    if [ ! -f ".env" ]; then
            echo "No .env file found."
            echo "Make sure the .env file exists in this folder before launching."
            read -p "Press Return to exit."
            exit 1
    fi

    echo "Launching Tweetables..."
    source venv/bin/activate
    python3 Main.py
    echo ""
    read -p "Press Return to close window."
    exit 0
fi

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


#Step 5: Installation complete and launching app - Auto Launch

    echo "Installation complete."
    echo "Launching Tweetables..."
    python3 Main.py

echo ""
read -p "Press Return to close window"
