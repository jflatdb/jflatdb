"""
Schema migration operations for transforming database records
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any
from .utils.logger import Logger


class MigrationError(Exception):
    """Raised when a migration operation fails"""
    pass


class SchemaMigration:
    """
    Performs schema migration operations on dataset.

    Supports:
    - add_field: Add new field with default value
    - remove_field: Remove field from all records
    - rename_field: Rename existing field
    - set_default: Fill missing field values with default
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Initialize migration engine with dataset.

        Args:
            data: List of records to migrate
        """
        self.data = data
        self.logger = Logger()

    def _resolve_default_value(self, default_value):
        """
        Resolve special default value keywords.

        Supported keywords:
        - NOW() -> current timestamp
        - UUID() -> random UUID string
        - EMPTY_STRING() -> ""
        - ZERO() -> 0
        - FALSE() -> False
        - EMPTY_LIST() -> []
        - EMPTY_DICT() -> {}

        Args:
            default_value: Value or keyword string

        Returns:
            Resolved value
        """
        if isinstance(default_value, str):
            if default_value == "NOW()":
                return datetime.now().isoformat()
            elif default_value == "UUID()":
                return str(uuid.uuid4())
            elif default_value == "EMPTY_STRING()":
                return ""
            elif default_value == "ZERO()":
                return 0
            elif default_value == "FALSE()":
                return False
            elif default_value == "EMPTY_LIST()":
                return []
            elif default_value == "EMPTY_DICT()":
                return {}

        return default_value

    def add_field(self, field_name: str, default_value=None):
        """
        Add a new field to all records.

        Args:
            field_name: Name of the field to add
            default_value: Default value for the new field (supports special keywords)

        Raises:
            MigrationError: If field already exists in some records
        """
        if not field_name:
            raise MigrationError("Field name cannot be empty")

        self.logger.info(f"Migration: Adding field '{field_name}' with default '{default_value}'")

        for record in self.data:
            if field_name in record:
                self.logger.warn(f"Field '{field_name}' already exists in some records, skipping those")
                continue
            record[field_name] = self._resolve_default_value(default_value)

        self.logger.info(f"Migration: Added field '{field_name}' to {len(self.data)} records")

    def remove_field(self, field_name: str):
        """
        Remove a field from all records.

        Args:
            field_name: Name of the field to remove

        Raises:
            MigrationError: If field name is empty
        """
        if not field_name:
            raise MigrationError("Field name cannot be empty")

        self.logger.info(f"Migration: Removing field '{field_name}'")

        removed_count = 0
        for record in self.data:
            if field_name in record:
                del record[field_name]
                removed_count += 1

        self.logger.info(f"Migration: Removed field '{field_name}' from {removed_count} records")

    def rename_field(self, old_name: str, new_name: str):
        """
        Rename a field in all records.

        Args:
            old_name: Current field name
            new_name: New field name

        Raises:
            MigrationError: If names are invalid or new_name already exists
        """
        if not old_name or not new_name:
            raise MigrationError("Field names cannot be empty")

        if old_name == new_name:
            raise MigrationError("Old and new field names must be different")

        self.logger.info(f"Migration: Renaming field '{old_name}' to '{new_name}'")

        renamed_count = 0
        for record in self.data:
            if old_name in record:
                if new_name in record:
                    raise MigrationError(
                        f"Cannot rename '{old_name}' to '{new_name}': "
                        f"'{new_name}' already exists in record"
                    )
                record[new_name] = record.pop(old_name)
                renamed_count += 1

        self.logger.info(f"Migration: Renamed field in {renamed_count} records")

    def set_default(self, field_name: str, default_value=None):
        """
        Set default value for missing or None field values.

        Only updates records where field is missing or None.

        Args:
            field_name: Name of the field
            default_value: Default value to set (supports special keywords)

        Raises:
            MigrationError: If field name is empty
        """
        if not field_name:
            raise MigrationError("Field name cannot be empty")

        self.logger.info(f"Migration: Setting default for field '{field_name}' to '{default_value}'")

        updated_count = 0
        for record in self.data:
            if field_name not in record or record[field_name] is None:
                record[field_name] = self._resolve_default_value(default_value)
                updated_count += 1

        self.logger.info(f"Migration: Set default for '{field_name}' in {updated_count} records")

    def get_data(self):
        """
        Get migrated data.

        Returns:
            List of migrated records
        """
        return self.data
