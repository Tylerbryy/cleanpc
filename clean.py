import os
import shutil
import subprocess
import sys
import importlib
import logging
from datetime import datetime

def install_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Install required packages
for package in ['rich', 'psutil']:
    install_package(package)

import psutil
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.logging import RichHandler

console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")

total_cleaned = 0

def clear_directory(directory):
    global total_cleaned
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    total_cleaned += file_size
                    logger.info(f"Removed file: {file_path}")
                except Exception as e:
                    logger.error(f"Error removing file {file_path}: {str(e)}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    dir_size = sum(os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)))
                    shutil.rmtree(dir_path)
                    total_cleaned += dir_size
                    logger.info(f"Removed directory: {dir_path}")
                except Exception as e:
                    logger.error(f"Error removing directory {dir_path}: {str(e)}")

def clear_temp_files():
    temp_dirs = []
    if sys.platform == 'darwin':  # macOS
        temp_dirs = [
            os.path.expanduser('~/Library/Caches'),
            os.path.expanduser('~/Library/Logs'),
            os.path.expanduser('~/Library/Application Support/CrashReporter'),
            '/tmp',
            '/var/tmp'
        ]
    elif sys.platform == 'win32':  # Windows
        temp_dirs = [
            os.path.expanduser('~\\AppData\\Local\\Temp'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\INetCache'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\WER'),
            os.environ.get('TEMP'),
            os.environ.get('TMP')
        ]
    for temp_dir in temp_dirs:
        logger.info(f"Clearing temporary files in {temp_dir}")
        clear_directory(temp_dir)

def clear_trash():
    if sys.platform == 'darwin':  # macOS
        trash_path = os.path.expanduser('~/.Trash')
        logger.info("Clearing macOS Trash")
        clear_directory(trash_path)
    elif sys.platform == 'win32':  # Windows
        import winshell
        try:
            logger.info("Clearing Windows Recycle Bin")
            recycle_bin = winshell.recycle_bin()
            global total_cleaned
            total_cleaned += sum(item.size() for item in recycle_bin)
            recycle_bin.empty(confirm=False, show_progress=False, sound=False)
        except Exception as e:
            logger.error(f"Error clearing Recycle Bin: {str(e)}")

def clear_browser_data():
    if sys.platform == 'darwin':  # macOS
        browsers = {
            'Chrome': '~/Library/Application Support/Google/Chrome/Default',
            'Firefox': '~/Library/Application Support/Firefox/Profiles',
            'Safari': '~/Library/Safari'
        }
    elif sys.platform == 'win32':  # Windows
        browsers = {
            'Chrome': '~\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
            'Firefox': '~\\AppData\\Local\\Mozilla\\Firefox\\Profiles',
            'Edge': '~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default'
        }
    
    for browser, path in browsers.items():
        full_path = os.path.expanduser(path)
        if os.path.exists(full_path):
            logger.info(f"Clearing {browser} data")
            clear_directory(os.path.join(full_path, 'Cache'))
            clear_directory(os.path.join(full_path, 'GPUCache'))

def optimize_disk():
    if sys.platform == 'darwin':  # macOS
        try:
            logger.info("Verifying and repairing disk")
            subprocess.call(['diskutil', 'verifyVolume', '/'])
            subprocess.call(['diskutil', 'repairVolume', '/'])
        except Exception as e:
            logger.error(f"Error optimizing disk: {str(e)}")
    elif sys.platform == 'win32':  # Windows
        try:
            logger.info("Running disk cleanup")
            subprocess.call(['cleanmgr', '/sagerun:1'])
            logger.info("Optimizing drives")
            subprocess.call(['defrag', '/C', '/O'])
        except Exception as e:
            logger.error(f"Error optimizing disk: {str(e)}")

def clear_system_logs():
    if sys.platform == 'darwin':  # macOS
        log_dirs = ['/var/log', '/Library/Logs']
    elif sys.platform == 'win32':  # Windows
        log_dirs = [os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\WER')]
    
    for log_dir in log_dirs:
        logger.info(f"Clearing system logs in {log_dir}")
        clear_directory(log_dir)

def is_admin():
    if sys.platform == 'win32':  # Windows
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.total, disk.used, disk.free

def main():
    if not is_admin():
        console.print(Panel.fit("Please run this script with administrator/root privileges.", title="Error", border_style="red"))
        return

    if sys.platform not in ['darwin', 'win32']:
        console.print(Panel.fit("Unsupported operating system.", title="Error", border_style="red"))
        return

    os_name = "macOS" if sys.platform == 'darwin' else "Windows"
    console.print(Panel.fit(f"Running {os_name} cleaning tasks...", title="System Cleaner", border_style="green"))

    total_before, used_before, _ = get_disk_usage()

    tasks = [
        ("Clearing temporary files", clear_temp_files),
        ("Clearing Trash/Recycle Bin", clear_trash),
        ("Clearing browser data", clear_browser_data),
        ("Clearing system logs", clear_system_logs),
        ("Optimizing disk", optimize_disk)
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        overall_task = progress.add_task("[green]Overall progress", total=len(tasks))
        for task_name, task_func in tasks:
            task = progress.add_task(task_name, total=1)
            task_func()
            progress.update(task, advance=1)
            progress.update(overall_task, advance=1)

    _, used_after, _ = get_disk_usage()
    space_freed = used_before - used_after

    results_table = Table(title="Cleaning Results")
    results_table.add_column("Metric", style="cyan")
    results_table.add_column("Value", style="magenta")
    results_table.add_row("Total data cleaned", f"{total_cleaned / (1024 * 1024):.2f} MB")
    results_table.add_row("Total disk space freed", f"{space_freed / (1024 * 1024):.2f} MB")
    results_table.add_row("Disk usage before", f"{used_before / total_before:.2%}")
    results_table.add_row("Disk usage after", f"{used_after / total_before:.2%}")

    console.print(results_table)

    console.print(Panel.fit("Cleaning completed successfully!", title="System Cleaner", border_style="green"))

if __name__ == '__main__':
    main()
