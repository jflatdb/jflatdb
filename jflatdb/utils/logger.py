"""
Logging system
"""

import time,os

class Logger:
    def __init__(self, logfile='db.log'):
        self.folder = 'logs'
        self.logfile = os.path.join(self.folder, logfile)
        os.makedirs(self.folder, exist_ok=True)  # Ensure 'logs/' exists

    def log(self, level, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"[{timestamp}] [{level.upper()}] {message}"
        print(formatted)
        with open(self.logfile, 'a') as f:
            f.write(formatted + "\n")

    def info(self, message): self.log('info', message)
    def warn(self, message): self.log('warn', message)
    def error(self, message): self.log('error', message)
