import os
import shutil
import subprocess
import sys
import importlib
from colorama import init, Fore, Style

def install_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_package('colorama')
init()

total_cleaned = 0

def clear_directory(directory):
    global total_cleaned
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    total_cleaned += file_size
                except:
                    pass
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    total_cleaned += sum(os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path))
                    shutil.rmtree(dir_path)
                except:
                    pass

def clear_temp_files():
    temp_dirs = []
    if sys.platform == 'darwin':  # macOS
        temp_dirs = [
            os.path.expanduser('~/Library/Caches'),
            os.path.expanduser('~/Library/Logs/DiagnosticReports'),
            os.path.expanduser('~/Library/Application Support/CrashReporter')
        ]
    elif sys.platform == 'win32':  # Windows
        temp_dirs = [
            os.path.expanduser('~\\AppData\\Local\\Temp'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files')
        ]
    for temp_dir in temp_dirs:
        clear_directory(temp_dir)

def clear_trash():
    if sys.platform == 'darwin':  # macOS
        trash_path = os.path.expanduser('~/.Trash')
        clear_directory(trash_path)
    elif sys.platform == 'win32':  # Windows
        install_package('winshell')
        import winshell
        try:
            recycle_bin = winshell.recycle_bin()
            global total_cleaned
            total_cleaned += sum(item.size for item in recycle_bin)
            recycle_bin.empty(confirm=False, show_progress=False, sound=False)
        except:
            pass

def optimize_disk():
    if sys.platform == 'darwin':  # macOS
        try:
            subprocess.call(['diskutil', 'verifyVolume', '/'])
        except:
            pass
    elif sys.platform == 'win32':  # Windows
        try:
            subprocess.call(['cleanmgr', '/sagerun:1'])
            subprocess.call(['defrag', '/C', '/U'])
        except:
            pass

def is_admin():
    if sys.platform == 'win32':  # Windows
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return True

def main():
    if sys.platform == 'darwin':  # macOS
        print(Fore.GREEN + "Running macOS cleaning tasks..." + Style.RESET_ALL)
    elif sys.platform == 'win32':  # Windows
        if not is_admin():
            print(Fore.RED + "Please run this script with administrator privileges." + Style.RESET_ALL)
            return
        print(Fore.GREEN + "Running Windows cleaning tasks..." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Unsupported operating system." + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Clearing temporary files..." + Style.RESET_ALL)
    clear_temp_files()
    print(Fore.CYAN + "Clearing Trash/Recycle Bin..." + Style.RESET_ALL)
    clear_trash()
    print(Fore.CYAN + "Optimizing disk..." + Style.RESET_ALL)
    optimize_disk()

    print(Fore.GREEN + "Cleaning completed successfully!" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total amount of data cleaned: {total_cleaned / (1024 * 1024):.2f} MB" + Style.RESET_ALL)

if __name__ == '__main__':
    main()