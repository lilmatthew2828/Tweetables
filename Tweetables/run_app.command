#!/bin/bash

# run_app.command: Tweetables Mac Launcher
# Purpose: Runs application on macOS by activating VE and launching Main.py
# Creator: Day Ekoi

echo "______________________"
echo "Launching Tweetables"
echo "______________________"

# Step 1: Verify VE exists
    if [ ! -d "venv" ]; 
    then
        echo "Virtual Environment not found."
        echo "Please run install_mac.command first"
        read -p "Press Return to exit"
        exit 1
    fi

# Step 2: Activate the VE that was created 
    source venv/bin/activate

# Step 3: Launch the Tweetable Application
    python3 Main.py

# Step 4: Keep Terminal open
    echo ""
    read -p "Press Return to close window"
