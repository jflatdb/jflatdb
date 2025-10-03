"""
File I/O operations with atomic write support
"""

import os
import tempfile


class Storage:
    def __init__(self, filename):
        self.folder = 'data'
        self.filepath = os.path.join(self.folder, filename)
        self.wal_path = os.path.join(self.folder, f"{filename}.wal")
        os.makedirs(self.folder, exist_ok=True)  # Ensure 'data/' exists

    def read(self):
        if not os.path.exists(self.filepath):
            return ""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def write(self, content):
        """
        Atomic write using write-ahead log and temp file.

        Process:
        1. Write to WAL (Write-Ahead Log)
        2. Write to temporary file
        3. Atomically rename temp file to actual file
        4. Remove WAL on success

        This ensures crash safety and atomicity.
        """
        # Write to WAL first
        self._write_wal(content)

        # Write to temporary file in same directory (ensures same filesystem)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=self.folder,
            prefix='.tmp_',
            suffix='.json'
        )

        try:
            # Write content to temp file
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                f.write(content)

            # Atomically replace the original file
            # os.replace is atomic on both Unix and Windows
            os.replace(temp_path, self.filepath)

            # Remove WAL after successful write
            self._remove_wal()

        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def _write_wal(self, content):
        """Write content to Write-Ahead Log"""
        with open(self.wal_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _remove_wal(self):
        """Remove Write-Ahead Log after successful write"""
        try:
            if os.path.exists(self.wal_path):
                os.unlink(self.wal_path)
        except OSError:
            pass

    def has_wal(self):
        """Check if WAL exists (indicates incomplete previous write)"""
        return os.path.exists(self.wal_path)

    def recover_from_wal(self):
        """
        Recover database from WAL if it exists.

        This should be called during database initialization to handle
        crash recovery.

        Returns:
            bool: True if recovery was performed, False otherwise
        """
        if not self.has_wal():
            return False

        try:
            # Read content from WAL
            with open(self.wal_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Write to main file
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            # Remove WAL
            self._remove_wal()

            return True

        except Exception:
            # If recovery fails, keep WAL for manual intervention
            return False
