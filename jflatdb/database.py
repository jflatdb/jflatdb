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
        self.data = self.load()
        self.query_engine = QueryEngine(self.data)
        self.logger.info("Database initialized") # test logger

    def load(self):
        """Load database contents from storage with robust error handling.

        Behavior:
        - If the file does not exist: log a warning and return an empty list.
        - If the file is empty: log a warning and return an empty list.
        - If decryption/parsing fails: log an error and raise RuntimeError.
        """
        try:
            if not os.path.exists(self.storage.filepath):
                self.logger.warn("Database file not found, initializing empty dataset")
                return []

            raw = self.storage.read()
            if not raw:
                self.logger.warn("Database file is empty, initializing empty dataset")
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
        self.logger.info(f"Inserted record: {record}") # Logger Test
        self.indexer.build(self.data)
        self.cache.invalidate()  # Invalidate cache on insert
        self.save()

    def find(self, query: dict):
        # Try to get from cache first
        cached_result = self.cache.get(query)
        if cached_result is not None:
            return cached_result

        # Cache miss - execute query
        result = self.indexer.query(self.data, query)

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
        self.data = [d for d in self.data if not all(d[k] == v for k, v in query.items())]
        self.cache.invalidate()  # Invalidate cache on delete
        self.save()
        
    # ----------- BUILT-IN QUERY FUNCTIONS ------------
    def min(self, column):
        return self.query_engine.min(column)

    def max(self, column):
        return self.query_engine.max(column)

    def avg(self, column):
        return self.query_engine.avg(column)

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