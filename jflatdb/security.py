"""
Basic encryption / hashing
"""

import time, os, hashlib

class Security:
    def __init__(self, password):
        self.key = sum(ord(c) for c in password)

    def encrypt(self, data: list):
        raw = str(data)
        return ''.join(chr(ord(c) ^ self.key) for c in raw)

    def decrypt(self, enc: str):
        if not enc: return []
        raw = ''.join(chr(ord(c) ^ self.key) for c in enc)
        return eval(raw)  # Safe only in controlled usage
    
    def _generate_id(self) -> str:
        """Generate unique document ID"""
        timestamp = str(int(time.time() * 1000000))
        random_part = hashlib.md5(os.urandom(16)).hexdigest()[:8]
        return f"{timestamp}_{random_part}"