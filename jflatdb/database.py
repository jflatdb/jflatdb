"""
Main JSONDatabase class
"""

import os

from .storage import Storage
from .schema import Schema
from .security import Security
from .indexer import Indexer
from .query_engine import QueryEngine
from .query_cache import QueryCache
from .transaction import Transaction
from .schema_migration import SchemaMigration
from .schema_version import SchemaVersion
from .utils.logger import Logger


class Database:
    def __init__(self, path, password, cache_enabled=True, cache_size=100):
        self.logger = Logger()
        self.path = path
        self.storage = Storage(path)
        self.schema = Schema()
        self.security = Security(password)
        self.indexer = Indexer()
        self.cache = QueryCache(max_size=cache_size, enabled=cache_enabled)

        # Initialize schema version tracking
        db_name = os.path.splitext(os.path.basename(path))[0]
        self.schema_version = SchemaVersion(
            storage_folder=self.storage.folder,
            db_name=f'{db_name}_schema'
        )

        # Perform WAL recovery if needed
        if self.storage.has_wal():
            self.logger.warn("Incomplete transaction detected, recovering from WAL")
            if self.storage.recover_from_wal():
                self.logger.info("WAL recovery successful")
            else:
                self.logger.error("WAL recovery failed")

        self.data = self.load()
        self.query_engine = QueryEngine(self.data)
        self.logger.info("Database initialized")  # test logger

    def load(self):
        """Load database contents from storage with robust error handling.

        Behavior:
        - If the file does not exist: log a warning and return empty list.
        - If the file is empty: log a warning and return an empty list.
        - If decryption/parsing fails: log error and raise RuntimeError.
        """
        try:
            if not os.path.exists(self.storage.filepath):
                self.logger.warn(
                    "Database file not found, initializing empty dataset"
                )
                return []

            raw = self.storage.read()
            if not raw:
                self.logger.warn(
                    "Database file is empty, initializing empty dataset"
                )
                return []

            return self.security.decrypt(raw)
        except Exception as e:
            self.logger.error(f"Failed to load database: {e}")
            raise RuntimeError("Database file is corrupt or unreadable") from e

    def save(self):
        encrypted = self.security.encrypt(self.data)
        self.storage.write(encrypted)
        self.query_engine = QueryEngine(self.data)

    def insert(self, record: dict):
        self.schema.validate(record, self.data)
        self.data.append(record)
        self.logger.info(f"Inserted record: {record}")  # Logger Test
        self.indexer.build(self.data)
        self.cache.invalidate()  # Invalidate cache on insert
        self.save()

    def find(self, query: dict):
        # Try to get from cache first
        cached_result = self.cache.get(query)
        if cached_result is not None:
            return cached_result

        # Cache miss - execute query
        result = self.indexer.query(query)

        # Store in cache
        self.cache.set(query, result)

        return result

    def update(self, query, updates):
        found = self.find(query)
        for item in found:
            item.update(updates)
        self.cache.invalidate()  # Invalidate cache on update
        self.save()

    def delete(self, query):
        self.data = [
            d for d in self.data
            if not all(d[k] == v for k, v in query.items())
        ]
        self.cache.invalidate()  # Invalidate cache on delete
        self.save()

    # ----------- BUILT-IN QUERY FUNCTIONS ------------
    def min(self, column):
        return self.query_engine.min(column)

    def max(self, column):
        return self.query_engine.max(column)

    def avg(self, column):
        return self.query_engine.avg(column)

    def sum(self, column):
        return self.query_engine.sum(column)

    def count(self, column=None):
        return self.query_engine.count(column)

    def between(self, column, low, high):
        return self.query_engine.between(column, low, high)

    def group_by(self, column):
        return self.query_engine.group_by(column)

    # ----------- CACHE MANAGEMENT METHODS ------------
    def get_cache_stats(self):
        """Get cache statistics including hits, misses, and hit rate"""
        return self.cache.get_stats()

    def clear_cache(self):
        """Manually clear the query cache"""
        self.cache.clear()

    def enable_cache(self):
        """Enable query caching"""
        self.cache.enable()

    def disable_cache(self):
        """Disable query caching"""
        self.cache.disable()

    # ----------- TRANSACTION SUPPORT ------------
    def transaction(self):
        """
        Create a new transaction context.

        Returns:
            Transaction: A new transaction instance

        Example:
            with db.transaction() as txn:
                txn.insert({"id": 1, "name": "Alice"})
                txn.insert({"id": 2, "name": "Bob"})
                # Both inserts committed atomically
        """
        return Transaction(self)

    # ----------- SCHEMA MIGRATION SUPPORT ------------
    def migrate_schema(self, migration_callback, migration_name=''):
        """
        Perform schema migration using callback function.

        Args:
            migration_callback: Function that takes SchemaMigration instance
            migration_name: Optional description of the migration

        Example:
            def add_timestamps(migration):
                migration.add_field('created_at', 'NOW()')
                migration.add_field('updated_at', 'NOW()')

            db.migrate_schema(add_timestamps, 'Add timestamp fields')
        """
        self.logger.info(f"Starting schema migration: {migration_name}")

        # Create migration instance with current data
        migration = SchemaMigration(self.data)

        # Execute migration callback
        migration_callback(migration)

        # Get migrated data
        self.data = migration.get_data()

        # Increment schema version
        self.schema_version.increment_version(migration_name)

        # Invalidate cache and save
        self.cache.invalidate()
        self.save()

        self.logger.info(
            f"Migration complete. Schema version: {self.schema_version.get_version()}"
        )

    def get_schema_version(self):
        """Get current schema version number"""
        return self.schema_version.get_version()

    def get_migration_history(self):
        """Get full migration history"""
        return self.schema_version.get_migration_history()
