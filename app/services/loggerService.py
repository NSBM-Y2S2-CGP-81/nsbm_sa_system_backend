import colorama
from datetime import datetime
import os
import pathlib

class LoggerService:
    def __init__(self):
        colorama.init(autoreset=True)
        # Create log directory in user's home directory
        log_dir = os.path.expanduser("~/.nsbm-sa-logs")
        pathlib.Path(log_dir).mkdir(exist_ok=True)
        self.log_file = os.path.join(log_dir, "log.txt")

        # Create log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                pass

        # Make sure it's writable
        try:
            os.chmod(self.log_file, 0o666)  # More portable than system commands
        except:
            pass

        self.saveToLogFile("Logger Service Initialized")

    def saveToLogFile(self, message: str):
        try:
            with open(self.log_file, "a") as log_file:
                log_file.write(f"{datetime.now()} - {message}\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def info(self, message: str):
        formatted = colorama.Fore.CYAN + "[INFO] " + message
        print(formatted)
        self.saveToLogFile(f'[INFO]: {message}')

    def error(self, message: str):
        formatted = colorama.Fore.RED + "[ERROR] " + message
        print(formatted)
        self.saveToLogFile(f'[ERROR]: {message}')

    def success(self, message: str):
        formatted = colorama.Fore.GREEN + "[SUCCESS] " + message
        print(formatted)
        self.saveToLogFile(f'[SUCCESS]: {message}')

    def warning(self, message: str):
        formatted = colorama.Fore.YELLOW + "[WARNING] " + message
        print(formatted)
        self.saveToLogFile(f'[WARNING]: {message}')
