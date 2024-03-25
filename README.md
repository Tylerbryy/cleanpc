# System Cleaner

This Python script is designed to clean and optimize your macOS or Windows system by performing various maintenance tasks. It clears temporary files, empties the Trash or Recycle Bin, and performs system-specific optimizations.

## Features

- Clears temporary files and caches on both macOS and Windows.
- Empties the Trash on macOS and the Recycle Bin on Windows.
- Runs disk verification on macOS using the `diskutil verifyVolume` command.
- Runs Disk Cleanup and disk defragmentation on Windows using the `cleanmgr` and `defrag` commands.
- Automatically installs the required libraries (colorama for both, and winshell for Windows) if they are not already installed.
- Provides colorful and informative output using the colorama library.

## Prerequisites

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

   The script will automatically install any missing libraries and start the cleaning process.
5. Follow the on-screen prompts and wait for the cleaning tasks to complete.

## Important Notes
- This script requires administrator privileges to run successfully.
- The script modifies system settings and performs system-level tasks. Exercise caution and ensure you understand the script's actions before running it on your system.
- It's highly recommended to backup important data before running any system cleaning or modification tools.
- The script uses the built-in Windows utilities cleanmgr and defrag, which may have different command-line options or may not be available on all versions of Windows.
- The script modifies the Windows registry. Incorrect modifications to the registry can cause system instability or other issues.
