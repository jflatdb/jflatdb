import os

import jflatdb.storage as storage_module
from jflatdb.database import Database
from jflatdb.query_cache import QueryCache


def _patch_storage_init_to_tmp(tmp_path, monkeypatch):
    def _init(self, filename):
        self.folder = str(tmp_path)
        self.filepath = os.path.join(self.folder, filename)
        os.makedirs(self.folder, exist_ok=True)
        return None

    monkeypatch.setattr(storage_module.Storage, "__init__", _init)


class TestQueryCacheBasics:
    """Test basic QueryCache functionality"""

    def test_cache_initialization(self):
        cache = QueryCache(max_size=50, enabled=True)
        assert cache.max_size == 50
        assert cache.enabled is True
        assert len(cache.cache) == 0
        assert cache.hits == 0
        assert cache.misses == 0

    def test_cache_set_and_get(self):
        cache = QueryCache()
        query = {"name": "Alice"}
        result = [{"name": "Alice", "age": 25}]

        # Cache miss
        assert cache.get(query) is None
        assert cache.misses == 1

        # Set cache
        cache.set(query, result)

        # Cache hit
        cached = cache.get(query)
        assert cached == result
        assert cache.hits == 1

    def test_cache_key_consistency(self):
        """Test that same query dict produces same cache key"""
        cache = QueryCache()

        # Different order, same content
        query1 = {"name": "Alice", "age": 25}
        query2 = {"age": 25, "name": "Alice"}

        result = [{"name": "Alice", "age": 25}]
        cache.set(query1, result)

        # Should hit cache with different key order
        assert cache.get(query2) == result

    def test_cache_invalidation(self):
        cache = QueryCache()
        cache.set({"name": "Alice"}, [{"name": "Alice"}])

        assert len(cache.cache) == 1
        cache.invalidate()
        assert len(cache.cache) == 0

    def test_cache_clear_alias(self):
        cache = QueryCache()
        cache.set({"name": "Alice"}, [{"name": "Alice"}])

        cache.clear()
        assert len(cache.cache) == 0

    def test_cache_enable_disable(self):
        cache = QueryCache()
        cache.set({"name": "Alice"}, [{"name": "Alice"}])

        # Disable cache
        cache.disable()
        assert cache.enabled is False
        assert len(cache.cache) == 0  # Should clear on disable

        # Get should return None when disabled
        assert cache.get({"name": "Alice"}) is None

        # Re-enable
        cache.enable()
        assert cache.enabled is True

    def test_lru_eviction(self):
        """Test LRU eviction when cache is full"""
        cache = QueryCache(max_size=3)

        cache.set({"id": 1}, [{"id": 1}])
        cache.set({"id": 2}, [{"id": 2}])
        cache.set({"id": 3}, [{"id": 3}])

        # Cache is full
        assert len(cache.cache) == 3

        # Add one more - should evict oldest (id=1)
        cache.set({"id": 4}, [{"id": 4}])
        assert len(cache.cache) == 3
        assert cache.get({"id": 1}) is None  # Evicted
        assert cache.get({"id": 4}) is not None  # Present

    def test_lru_access_updates_order(self):
        """Test that accessing an item moves it to end (most recent)"""
        cache = QueryCache(max_size=3)

        cache.set({"id": 1}, [{"id": 1}])
        cache.set({"id": 2}, [{"id": 2}])
        cache.set({"id": 3}, [{"id": 3}])

        # Access id=1 (moves it to end)
        cache.get({"id": 1})

        # Add new item - should evict id=2 (now oldest)
        cache.set({"id": 4}, [{"id": 4}])

        assert cache.get({"id": 1}) is not None  # Still present
        assert cache.get({"id": 2}) is None  # Evicted
        assert cache.get({"id": 3}) is not None  # Present
        assert cache.get({"id": 4}) is not None  # Present

    def test_cache_stats(self):
        cache = QueryCache(max_size=10)

        # Initial state
        stats = cache.get_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["size"] == 0
        assert stats["max_size"] == 10
        assert stats["enabled"] is True

        # Add and retrieve
        cache.set({"id": 1}, [{"id": 1}])
        cache.get({"id": 1})  # Hit
        cache.get({"id": 2})  # Miss

        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["size"] == 1
        assert stats["hit_rate"] == "50.00%"

    def test_reset_stats(self):
        cache = QueryCache()
        cache.set({"id": 1}, [{"id": 1}])
        cache.get({"id": 1})
        cache.get({"id": 2})

        assert cache.hits == 1
        assert cache.misses == 1

        cache.reset_stats()
        assert cache.hits == 0
        assert cache.misses == 0


class TestDatabaseCacheIntegration:
    """Test cache integration with Database class"""

    def test_database_cache_initialization(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database(
            'test.json', password='test', cache_enabled=True, cache_size=50
        )

        assert db.cache is not None
        assert db.cache.enabled is True
        assert db.cache.max_size == 50

    def test_database_cache_disabled(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test', cache_enabled=False)

        assert db.cache.enabled is False

    def test_query_caching_works(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        # Insert data
        db.insert({"id": 1, "name": "Alice"})
        db.insert({"id": 2, "name": "Bob"})

        # First query - cache miss
        result1 = db.find({"name": "Alice"})
        assert db.cache.misses == 1
        assert db.cache.hits == 0

        # Same query - cache hit
        result2 = db.find({"name": "Alice"})
        assert db.cache.hits == 1
        assert result1 == result2

    def test_cache_invalidation_on_insert(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        db.insert({"id": 1, "name": "Alice"})

        # Query to populate cache
        db.find({"name": "Alice"})
        assert len(db.cache.cache) > 0

        # Insert should invalidate cache
        db.insert({"id": 2, "name": "Bob"})
        assert len(db.cache.cache) == 0

    def test_cache_invalidation_on_update(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        db.insert({"id": 1, "name": "Alice", "age": 25})

        # Query to populate cache
        db.find({"name": "Alice"})
        assert len(db.cache.cache) > 0

        # Update should invalidate cache
        db.update({"name": "Alice"}, {"age": 26})
        assert len(db.cache.cache) == 0

    def test_cache_invalidation_on_delete(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        db.insert({"id": 1, "name": "Alice"})
        db.insert({"id": 2, "name": "Bob"})

        # Query to populate cache
        db.find({"name": "Alice"})
        assert len(db.cache.cache) > 0

        # Delete should invalidate cache
        db.delete({"name": "Bob"})
        assert len(db.cache.cache) == 0

    def test_cache_management_methods(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        db.insert({"id": 1, "name": "Alice"})

        # Query to populate cache
        db.find({"name": "Alice"})

        # Get stats
        stats = db.get_cache_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 1

        # Clear cache
        db.clear_cache()
        assert len(db.cache.cache) == 0

        # Disable cache
        db.disable_cache()
        assert db.cache.enabled is False

        # Enable cache
        db.enable_cache()
        assert db.cache.enabled is True

    def test_multiple_different_queries_cached(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test', cache_size=10)

        db.insert({"id": 1, "name": "Alice", "age": 25})
        db.insert({"id": 2, "name": "Bob", "age": 30})
        db.insert({"id": 3, "name": "Charlie", "age": 35})

        # Different queries
        db.find({"name": "Alice"})
        db.find({"age": 30})
        db.find({})

        # All should be cached
        assert len(db.cache.cache) == 3

        # Repeat queries should hit cache
        db.find({"name": "Alice"})
        db.find({"age": 30})

        stats = db.get_cache_stats()
        assert stats["hits"] == 2

    def test_cache_with_operators(self, tmp_path, monkeypatch):
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        db.insert({"id": 1, "age": 20})
        db.insert({"id": 2, "age": 25})
        db.insert({"id": 3, "age": 30})

        # Query with operators
        result1 = db.find({"age": {"$gt": 22}})
        assert db.cache.misses == 1

        # Same query should hit cache
        result2 = db.find({"age": {"$gt": 22}})
        assert db.cache.hits == 1
        assert result1 == result2
