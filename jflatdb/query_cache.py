"""
Query caching layer for jflatdb
Implements in-memory caching with LRU eviction policy
"""

import json
from collections import OrderedDict


class QueryCache:
    """
    In-memory cache for query results with LRU eviction policy.

    Attributes:
        max_size (int): Maximum number of cached queries
        enabled (bool): Whether caching is enabled
        cache (OrderedDict): Ordered dictionary storing cached results
        hits (int): Number of cache hits
        misses (int): Number of cache misses
    """

    def __init__(self, max_size=100, enabled=True):
        """
        Initialize the query cache.

        Args:
            max_size (int): Maximum number of queries to cache (default: 100)
            enabled (bool): Enable/disable caching (default: True)
        """
        self.max_size = max_size
        self.enabled = enabled
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def _make_key(self, query: dict) -> str:
        """
        Convert a query dictionary into a hashable cache key.

        Args:
            query (dict): The query dictionary

        Returns:
            str: JSON string representation of the query
        """
        # Sort keys to ensure consistent cache keys for same query
        return json.dumps(query, sort_keys=True)

    def get(self, query: dict):
        """
        Retrieve cached result for a query.

        Args:
            query (dict): The query to look up

        Returns:
            list or None: Cached results if found, None otherwise
        """
        if not self.enabled:
            return None

        key = self._make_key(query)

        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        return None

    def set(self, query: dict, result: list):
        """
        Store query result in cache.

        Args:
            query (dict): The query that was executed
            result (list): The query result to cache
        """
        if not self.enabled:
            return

        key = self._make_key(query)

        # If key exists, move to end
        if key in self.cache:
            self.cache.move_to_end(key)

        # Store the result (make a copy to avoid mutation issues)
        self.cache[key] = result.copy() if result else []

        # Evict oldest entry if cache is full (LRU)
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)  # Remove first (oldest) item

    def invalidate(self):
        """
        Clear all cached queries.
        Called when database is modified (insert/update/delete).
        """
        self.cache.clear()

    def clear(self):
        """Alias for invalidate()"""
        self.invalidate()

    def enable(self):
        """Enable caching"""
        self.enabled = True

    def disable(self):
        """Disable caching and clear cache"""
        self.enabled = False
        self.cache.clear()

    def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            dict: Statistics including hits, misses, size, and hit rate
        """
        total_requests = self.hits + self.misses
        hit_rate = (
            (self.hits / total_requests * 100) if total_requests > 0 else 0
        )

        return {
            "enabled": self.enabled,
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%"
        }

    def reset_stats(self):
        """Reset cache statistics (hits and misses)"""
        self.hits = 0
        self.misses = 0
