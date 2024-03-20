import os
import shutil
import winreg
import subprocess
import ctypes
import sys
import importlib

def install_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_package('winshell')
install_package('colorama')

from colorama import init, Fore, Style

init()

total_cleaned = 0

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear_temp_files():
    global total_cleaned
    temp_dirs = [os.path.expanduser('~\\AppData\\Local\\Temp'),
                 os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files')]

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

def clear_recycle_bin():
    global total_cleaned
    try:
        import winshell
        recycle_bin = winshell.recycle_bin()
        total_cleaned += sum(item.size for item in recycle_bin)
        recycle_bin.empty(confirm=False, show_progress=False, sound=False)
    except:
        pass

def disk_cleanup():
    try:
        subprocess.call(['cleanmgr', '/sagerun:1'])
    except:
        pass

def defragment_disk():
    try:
        subprocess.call(['defrag', '/C', '/U'])
    except:
        pass

def remove_outdated_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VolumeCaches')
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(subkey, '')
            winreg.CloseKey(subkey)
        winreg.CloseKey(key)
    except:
        pass

if __name__ == '__main__':
    if is_admin():
        print(Fore.GREEN + "Running PC cleaning tasks..." + Style.RESET_ALL)

        print(Fore.CYAN + "Clearing temporary files..." + Style.RESET_ALL)
        clear_temp_files()

        print(Fore.CYAN + "Clearing Recycle Bin..." + Style.RESET_ALL)
        clear_recycle_bin()

        print(Fore.CYAN + "Running Disk Cleanup..." + Style.RESET_ALL)
        disk_cleanup()

        print(Fore.CYAN + "Defragmenting disk..." + Style.RESET_ALL)
        defragment_disk()

        print(Fore.CYAN + "Removing outdated registry entries..." + Style.RESET_ALL)
        remove_outdated_registry()

        print(Fore.GREEN + "PC cleaning completed successfully!" + Style.RESET_ALL)
        print(Fore.GREEN + f"Total amount of data cleaned: {total_cleaned / (1024 * 1024):.2f} MB" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Please run this script with administrator privileges." + Style.RESET_ALL)