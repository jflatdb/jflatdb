"""
Schema version tracking and migration history management
"""

import os
import json
from datetime import datetime
from .utils.logger import Logger


class SchemaVersion:
    """
    Manages schema versioning and migration history.

    Stores metadata in schema_version.json to track:
    - Current schema version
    - Migration history
    - Timestamps for each migration
    """

    def __init__(self, storage_folder='data', db_name='schema_version'):
        """
        Initialize schema version tracker.

        Args:
            storage_folder: Folder where metadata is stored
            db_name: Name for the version metadata file
        """
        self.logger = Logger()
        self.storage_folder = storage_folder
        self.metadata_file = os.path.join(storage_folder, f'{db_name}.json')
        os.makedirs(storage_folder, exist_ok=True)

        self._metadata = self._load_metadata()

    def _load_metadata(self):
        """Load metadata from file or initialize if not exists"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load schema metadata: {e}")
                metadata = self._init_metadata()
                self._save_metadata_internal(metadata)
                return metadata
        else:
            # File doesn't exist, create it
            metadata = self._init_metadata()
            self._save_metadata_internal(metadata)
            return metadata

    def _init_metadata(self):
        """Initialize default metadata structure"""
        return {
            'version': 0,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'migrations': []
        }

    def _save_metadata_internal(self, metadata):
        """Internal method to save metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save schema metadata: {e}")
            raise

    def _save_metadata(self):
        """Save metadata to file"""
        self._save_metadata_internal(self._metadata)
        self.logger.info(f"Schema metadata saved (version: {self._metadata['version']})")

    def get_version(self):
        """
        Get current schema version.

        Returns:
            int: Current schema version number
        """
        return self._metadata['version']

    def increment_version(self, migration_name=''):
        """
        Increment schema version and record migration.

        Args:
            migration_name: Description of the migration
        """
        old_version = self._metadata['version']
        new_version = old_version + 1

        migration_record = {
            'from_version': old_version,
            'to_version': new_version,
            'name': migration_name,
            'timestamp': datetime.now().isoformat()
        }

        self._metadata['version'] = new_version
        self._metadata['updated_at'] = datetime.now().isoformat()
        self._metadata['migrations'].append(migration_record)

        self._save_metadata()
        self.logger.info(f"Schema version updated: {old_version} -> {new_version}")

    def get_migration_history(self):
        """
        Get full migration history.

        Returns:
            list: List of migration records
        """
        return self._metadata['migrations'].copy()

    def get_metadata(self):
        """
        Get complete metadata.

        Returns:
            dict: Full metadata including version and history
        """
        return self._metadata.copy()

    def reset(self):
        """
        Reset version to 0 and clear history.

        WARNING: This should only be used for testing or complete schema resets.
        """
        self._metadata = self._init_metadata()
        self._save_metadata()
        self.logger.warn("Schema version reset to 0")
