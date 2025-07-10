"""
File I/O operations
"""

import os

class Storage:
    def __init__(self, filename):
        self.folder = 'data'
        self.filepath = os.path.join(self.folder, filename)
        os.makedirs(self.folder, exist_ok=True)  # Ensure 'data/' exists

    def read(self):
        if not os.path.exists(self.filepath):
            return ""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def write(self, content):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(content)