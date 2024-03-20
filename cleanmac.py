import os
import shutil
import subprocess
import sys
import importlib

def install_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_package('colorama')

from colorama import init, Fore, Style

init()

total_cleaned = 0

def clear_temp_files():
    global total_cleaned
    temp_dirs = [
        os.path.expanduser('~/Library/Caches'),
        os.path.expanduser('~/Library/Logs/DiagnosticReports'),
        os.path.expanduser('~/Library/Application Support/CrashReporter')
    ]

    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir):
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

def clear_trash():
    global total_cleaned
    trash_path = os.path.expanduser('~/.Trash')
    if os.path.exists(trash_path):
        for root, dirs, files in os.walk(trash_path):
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

def optimize_disk():
    try:
        subprocess.call(['diskutil', 'verifyVolume', '/'])
    except:
        pass

if __name__ == '__main__':
    print(Fore.GREEN + "Running macOS cleaning tasks..." + Style.RESET_ALL)

    print(Fore.CYAN + "Clearing temporary files..." + Style.RESET_ALL)
    clear_temp_files()

    print(Fore.CYAN + "Clearing Trash..." + Style.RESET_ALL)
    clear_trash()

    print(Fore.CYAN + "Verifying disk..." + Style.RESET_ALL)
    optimize_disk()

    print(Fore.GREEN + "macOS cleaning completed successfully!" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total amount of data cleaned: {total_cleaned / (1024 * 1024):.2f} MB" + Style.RESET_ALL)