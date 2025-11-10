
# INSTALLATION INSTRUCTIONS

This document provides the installation steps for running the Tweetables application on both Windows and macOS. These instructions were created for the current project deliverables and do not replace the orginal README.

***Please read installation instructions in full***

##  Windows Installation

### 1. Download the Project 
Download or clone the **TWEETABLES** project folder to your computer

### 2. Run the Windows Installer 
Inside the Tweetables folder, double click: **install_windows.bat**

**install_windows.bat** will automatically:
- Create a Python Virtual Environment 
- Install all required packed from requirements.txt
- Launch the application

### 3. Running the App Again Later On
After installation, you can run the app anytime by double-clicking: **run_app.bat**

**run_app.bat** starts the program without reinstallation

## macOS Installation

### 1. Download the Project
Download or clone the **TWEETABLES** project folder.

### 2. Allow the Installer to Run ***(Important!)***
*Note: This step only needs to be done ***once****

Before double clicking the installer, open *Terminal* and run:

``` bash
chmod +x install_mac.command
```
### 4. Run the Mac Installer
Now double click: **install_mac.command**

This installer will automatically:
- Create a Virtual Environment
- Install dependences from requirements.txt
- Launch the Application

### 4a. Troubleshooting macOS Security Warning (Important)
macOS may display the messag:

"install_mac.command cannot be opened because Apple cannoy verify it is free of malware"

This is completely normal for all **.command** files not downloaded from the App Store.

To allow the installer to run:

1. Open **System Settings**
2. Go to **Privacy & Security**
3. Scroll down until you see a message saying the file was blocked
4. Click **Allow Anyway**
5. Double-click the file again, and choose **Open**

If you recieve a permissions error, run these commands in *Terminal*:
```bash

chmod +x install_mac.command
chmod +x run_app.command
```

This gives your Mac permission to execute the scripts.

If the installer continues to be blocked due to Apple's quarantine flag, you can remove the quarantine attribute by running these commands in *Terminal*

Only run these commands if macOS continues blocking the files after clicking "Allow Anyway" and running **chmod +x**

```bash
xattr -d com.apple.quarantine install_mac.command
xattr -d com.apple.quarantine run_app.command
```

### 5. Running the App Again Later On
To run Tweetables agin:

1. Give permission once (if needed):

```bash
chmod +x run_app.command
```
2. Double click: **run_app.command**


### Notes
- Python 3.10+ is required on btoh Windows or macOS
- Do **NOT** delete the *venv* folder after installation
- Internet connection is required the first time for dependecy installation

## Credits 

Created by: Day Ekoi

### Xpendables Team
- Brian Csehoski (PM)
- Day Ekoi 
- Aris Hill (Co-PM)
- Derrick Hollie
- Matthew Kilpatrick
- Tadarrio Marshall
- Daniel Ufua

