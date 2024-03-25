# System Cleaner

<<<<<<< HEAD
This Python script is designed to clean and optimize your macOS or Windows system by performing various maintenance tasks. It clears temporary files, empties the Trash or Recycle Bin, and performs system-specific optimizations.

## Features

- Clears temporary files and caches on both macOS and Windows.
- Empties the Trash on macOS and the Recycle Bin on Windows.
- Runs disk verification on macOS using the `diskutil verifyVolume` command.
- Runs Disk Cleanup and disk defragmentation on Windows using the `cleanmgr` and `defrag` commands.
- Automatically installs the required libraries (colorama for both, and winshell for Windows) if they are not already installed.
=======
This Python script is designed to clean and optimize your Windows or macOS system by performing various maintenance tasks. It clears temporary files, empties the Recycle Bin or Trash, and performs system-specific optimizations.

## Features

### Windows
- Clears temporary files from the user's Temp and Temporary Internet Files directories.
- Empties the Recycle Bin.
- Runs the Disk Cleanup utility to remove unnecessary files.
- Defragments the hard disk using the built-in defragmentation tool.
- Removes outdated registry entries related to the Windows Explorer volume caches.

### macOS
- Clears temporary files from various directories such as ~/Library/Caches, ~/Library/Logs/DiagnosticReports, and ~/Library/Application Support/CrashReporter.
- Empties the Trash directory (~/.Trash).
- Verifies the integrity of the main disk using the diskutil verifyVolume command.

### Common Features
- Automatically installs the required libraries (winshell and colorama for Windows, colorama for macOS) if they are not already installed.
>>>>>>> 3d8d9afe098af63c14b7dccb6a8752b095d0e8db
- Provides colorful and informative output using the colorama library.
- Calculates and displays the total amount of data cleaned at the end of the cleaning process.

## Prerequisites
<<<<<<< HEAD

- Python 3.x installed on your macOS or Windows system.
- Administrator privileges to run the script (required on Windows).

## Usage

1. Clone the repository or download the script file.
2. Open a terminal or command prompt.
   - On Windows, make sure to run the command prompt as an administrator.
3. Navigate to the directory where the script is located.
4. Run the following command:

   ```bash
   python cleaner.py
    ```
=======
- Python 3.x installed on your system.
- Administrator privileges (for Windows) or necessary permissions (for macOS) to run the script and perform system-level tasks.

## Usage
1. Clone the repository or download the script files (cleanwindows.py for Windows, cleanmac.py for macOS).
2. Open a command prompt or terminal with appropriate privileges.
3. Navigate to the directory where the script files are located.
4. Run the appropriate command for your operating system:
>>>>>>> 3d8d9afe098af63c14b7dccb6a8752b095d0e8db

   For Windows:
   ```
   python cleanwindows.py
   ```
   For macOS:
   ```
   python cleanmac.py
   ```
   The script will automatically install any missing libraries and start the cleaning process.
5. Follow the on-screen prompts and wait for the cleaning tasks to complete.

## Important Notes
- The scripts modify system settings and perform system-level tasks. Exercise caution and ensure you understand the scripts' actions before running them on your system.
- It's highly recommended to backup important data before running any system cleaning or modification tools.
- For Windows, the script uses the built-in utilities cleanmgr and defrag, which may have different command-line options or may not be available on all versions of Windows.
- For Windows, the script modifies the Windows registry. Incorrect modifications to the registry can cause system instability or other issues.
- For macOS, the script assumes you have Python and pip installed on your system.
