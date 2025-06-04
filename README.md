# MisType

**Typed in the wrong language?** Just hit a hotkey ⌨️ — MisType ✂️ cuts, converts, ✅ pastes the correct text, and switches the system language so you can keep typing like nothing happened! ⚡

## Overview

MisType is a lightweight utility for Windows that helps you recover from typing in the wrong keyboard layout (e.g., typing in Hebrew when you meant to type in English). With a single hotkey, MisType:

* Cuts the incorrectly typed text
* Converts it to the intended language
* Pastes the corrected text
* Switches your system's input language([github.com][1])

This seamless process allows you to continue typing without interruption.

## Features

* Instant text correction with a hotkey
* Automatic system input language switch
* Customizable dictionary for accurate conversions
* System tray integration for easy access([github.com][1])

## Installation

### Prerequisites

* Windows (10 / 11)
* Python 3.x installed

### Steps

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone https://github.com/TapChap/MisType.git
   cd MisType
   ```



2. **Install Dependencies**

   Ensure you have the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```



3. **Generate an executable file**

   generete the executable with the given pyinstaller script, run in terminal:

   ```bash
   build.bat
   ```
   after a short time an executable should appear in the project files.
   double click it to run the porgram in the background.

   The application will run in the background with a system tray icon for easy access.

## Usage

1. **Typing Correction**

   If you realize you've typed text in the wrong language, simply press the designated hotkey (default: `Ctrl + Alt + Z`). MisType will:

   * Cut the incorrect text
   * Convert it to the correct language
   * Paste the corrected text
   * Switch your system's input language

2. **System Tray Menu**

   Right-click the MisType icon in the system tray to access options such as:

   * Exiting the application
   * Changing hotkey configuration

## Customization

* **Dictionary Configuration**

  Modify `dictionary.py` to customize language mappings and improve conversion accuracy.

* **Hotkey Settings**

  Adjust the default hotkey combination in the `app.py` file to suit your preferences.
