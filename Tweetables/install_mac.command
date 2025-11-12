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

#Steo 4: Create .env file for Neo4j connection

#    echo "Setting up environement..."
#    cat <<EOT > .env
    # Environemnt variables for Neo4j Aura database 
#    NEO4J_URI="neo4j+s://f1c11ed7.databases.neo4j.io"
 #   NEO4J_USER=neo4j
 #   NEO4J_PASSWORD=YOUR_SHARED_TEAM_PASSWORD_HERE
 #   EOT

#Step 4: Installation complete and launching app

    echo "Installation complete."
    echo "Launching Tweetables..."
    python3 Main.py
