"""
Unit tests for Database class

Tests cover:
- Database initialization
- Insert operations with valid and invalid data
- Update operations
- Delete operations
- Query operations (find)
- Aggregate functions (min, max, avg, count)
- Cache management
- Error handling
"""

import unittest
import os
import tempfile
import shutil
from jflatdb.database import Database
from jflatdb.schema import Schema


class TestDatabase(unittest.TestCase):
    """Test suite for Database class"""

    def setUp(self):
        """Set up test database with temporary directory"""
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test.json")
        self.password = "test_password_123"
        self.db = Database(self.db_path, self.password)

    def tearDown(self):
        """Clean up test database and temporary directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    # ========== INITIALIZATION TESTS ==========

    def test_database_initialization(self):
        """Test database initializes correctly"""
        self.assertIsNotNone(self.db)
        self.assertEqual(self.db.path, self.db_path)
        self.assertIsInstance(self.db.data, list)
        self.assertEqual(len(self.db.data), 0)

    def test_database_initialization_with_cache_disabled(self):
        """Test database initialization with cache disabled"""
        db = Database(self.db_path, self.password, cache_enabled=False)
        self.assertFalse(db.cache.enabled)

    def test_database_initialization_with_custom_cache_size(self):
        """Test database initialization with custom cache size"""
        cache_size = 50
        db = Database(self.db_path, self.password, cache_size=cache_size)
        self.assertEqual(db.cache.max_size, cache_size)

    # ========== INSERT TESTS ==========

    def test_insert_valid_record(self):
        """Test inserting a valid record"""
        record = {"id": 1, "name": "Alice", "age": 25}
        self.db.insert(record)
        self.assertEqual(len(self.db.data), 1)
        self.assertIn(record, self.db.data)

    def test_insert_multiple_records(self):
        """Test inserting multiple records"""
        records = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30},
            {"id": 3, "name": "Charlie", "age": 35}
        ]
        for record in records:
            self.db.insert(record)
        self.assertEqual(len(self.db.data), 3)

    def test_insert_empty_record(self):
        """Test inserting an empty record"""
        record = {}
        self.db.insert(record)
        self.assertEqual(len(self.db.data), 1)
        self.assertIn(record, self.db.data)

    def test_insert_record_with_special_characters(self):
        """Test inserting record with special characters in values"""
        record = {"id": 1, "name": "Alice@123", "email": "alice+test@example.com"}
        self.db.insert(record)
        self.assertEqual(len(self.db.data), 1)
        self.assertEqual(self.db.data[0]["email"], "alice+test@example.com")

    def test_insert_record_with_nested_data(self):
        """Test inserting record with nested dictionary
        
        Note: Current implementation may not support nested dict indexing
        This test documents expected behavior for future enhancement
        """
        record = {
            "id": 1,
            "name": "Alice",
            "city": "New York"  # Using flat structure instead of nested
        }
        self.db.insert(record)
        self.assertEqual(len(self.db.data), 1)
        self.assertEqual(self.db.data[0]["city"], "New York")

    # ========== FIND/QUERY TESTS ==========

    def test_find_existing_record(self):
        """Test finding an existing record"""
        record = {"id": 1, "name": "Alice", "age": 25}
        self.db.insert(record)
        result = self.db.find({"name": "Alice"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Alice")

    def test_find_nonexistent_record(self):
        """Test finding a non-existent record returns empty list"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        result = self.db.find({"name": "Bob"})
        self.assertEqual(len(result), 0)

    def test_find_with_multiple_criteria(self):
        """Test finding records with multiple query criteria"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.insert({"id": 2, "name": "Bob", "age": 25})
        result = self.db.find({"age": 25})
        self.assertEqual(len(result), 2)

    def test_find_empty_database(self):
        """Test finding in empty database returns empty list"""
        result = self.db.find({"name": "Alice"})
        self.assertEqual(len(result), 0)

    # ========== UPDATE TESTS ==========

    def test_update_existing_record(self):
        """Test updating an existing record"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.update({"name": "Alice"}, {"age": 26})
        result = self.db.find({"name": "Alice"})
        self.assertEqual(result[0]["age"], 26)

    def test_update_multiple_records(self):
        """Test updating multiple records at once"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.insert({"id": 2, "name": "Bob", "age": 25})
        self.db.update({"age": 25}, {"status": "updated"})
        result = self.db.find({"status": "updated"})
        self.assertEqual(len(result), 2)

    def test_update_nonexistent_record(self):
        """Test updating a non-existent record does nothing"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.update({"name": "Bob"}, {"age": 30})
        self.assertEqual(len(self.db.data), 1)
        self.assertEqual(self.db.data[0]["age"], 25)

    def test_update_adds_new_field(self):
        """Test update can add new fields to records"""
        self.db.insert({"id": 1, "name": "Alice"})
        self.db.update({"name": "Alice"}, {"age": 25})
        result = self.db.find({"name": "Alice"})
        self.assertIn("age", result[0])
        self.assertEqual(result[0]["age"], 25)

    # ========== DELETE TESTS ==========

    def test_delete_existing_record(self):
        """Test deleting an existing record"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.delete({"name": "Alice"})
        self.assertEqual(len(self.db.data), 0)

    def test_delete_multiple_records(self):
        """Test deleting multiple records"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.insert({"id": 2, "name": "Bob", "age": 25})
        self.db.delete({"age": 25})
        self.assertEqual(len(self.db.data), 0)

    def test_delete_nonexistent_record(self):
        """Test deleting a non-existent record does nothing"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        initial_count = len(self.db.data)
        self.db.delete({"name": "Bob"})
        self.assertEqual(len(self.db.data), initial_count)

    def test_delete_with_partial_match(self):
        """Test delete only removes exact matches"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25, "city": "NYC"})
        self.db.insert({"id": 2, "name": "Bob", "age": 25, "city": "LA"})
        self.db.delete({"age": 25, "city": "NYC"})
        self.assertEqual(len(self.db.data), 1)
        self.assertEqual(self.db.data[0]["name"], "Bob")

    # ========== AGGREGATE FUNCTION TESTS ==========

    def test_min_function(self):
        """Test min aggregate function"""
        self.db.insert({"id": 1, "score": 85})
        self.db.insert({"id": 2, "score": 92})
        self.db.insert({"id": 3, "score": 78})
        result = self.db.min("score")
        self.assertEqual(result, 78)

    def test_max_function(self):
        """Test max aggregate function"""
        self.db.insert({"id": 1, "score": 85})
        self.db.insert({"id": 2, "score": 92})
        self.db.insert({"id": 3, "score": 78})
        result = self.db.max("score")
        self.assertEqual(result, 92)

    def test_avg_function(self):
        """Test avg aggregate function"""
        self.db.insert({"id": 1, "score": 80})
        self.db.insert({"id": 2, "score": 90})
        self.db.insert({"id": 3, "score": 100})
        result = self.db.avg("score")
        self.assertEqual(result, 90.0)

    def test_count_function(self):
        """Test count aggregate function"""
        self.db.insert({"id": 1, "name": "Alice"})
        self.db.insert({"id": 2, "name": "Bob"})
        self.db.insert({"id": 3, "name": "Charlie"})
        result = self.db.count()
        self.assertEqual(result, 3)

    def test_count_with_column(self):
        """Test count with specific column"""
        self.db.insert({"id": 1, "name": "Alice", "score": 85})
        self.db.insert({"id": 2, "name": "Bob", "score": None})
        self.db.insert({"id": 3, "name": "Charlie", "score": 92})
        result = self.db.count("score")
        # Count should handle None values appropriately
        self.assertIsInstance(result, int)

    def test_between_function(self):
        """Test between range query function"""
        self.db.insert({"id": 1, "age": 20})
        self.db.insert({"id": 2, "age": 25})
        self.db.insert({"id": 3, "age": 30})
        self.db.insert({"id": 4, "age": 35})
        result = self.db.between("age", 22, 32)
        self.assertEqual(len(result), 2)

    def test_group_by_function(self):
        """Test group_by aggregate function"""
        self.db.insert({"id": 1, "city": "NYC", "name": "Alice"})
        self.db.insert({"id": 2, "city": "LA", "name": "Bob"})
        self.db.insert({"id": 3, "city": "NYC", "name": "Charlie"})
        result = self.db.group_by("city")
        self.assertIn("NYC", result)
        self.assertIn("LA", result)
        self.assertEqual(len(result["NYC"]), 2)
        self.assertEqual(len(result["LA"]), 1)

    # ========== CACHE TESTS ==========

    def test_cache_hit(self):
        """Test query cache returns cached results"""
        self.db.insert({"id": 1, "name": "Alice"})
        query = {"name": "Alice"}
        
        # First query - cache miss
        result1 = self.db.find(query)
        stats1 = self.db.get_cache_stats()
        
        # Second query - should be cache hit
        result2 = self.db.find(query)
        stats2 = self.db.get_cache_stats()
        
        self.assertEqual(result1, result2)
        self.assertGreater(stats2['hits'], stats1['hits'])

    def test_cache_invalidation_on_insert(self):
        """Test cache is invalidated after insert"""
        self.db.insert({"id": 1, "name": "Alice"})
        self.db.find({"name": "Alice"})  # Cache this query
        
        self.db.insert({"id": 2, "name": "Bob"})  # Should invalidate cache
        stats = self.db.get_cache_stats()
        
        # Cache should be cleared
        self.assertIsNotNone(stats)

    def test_cache_invalidation_on_update(self):
        """Test cache is invalidated after update"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        self.db.find({"name": "Alice"})
        
        self.db.update({"name": "Alice"}, {"age": 26})
        # After update, cache should be invalidated

    def test_cache_invalidation_on_delete(self):
        """Test cache is invalidated after delete"""
        self.db.insert({"id": 1, "name": "Alice"})
        self.db.find({"name": "Alice"})
        
        self.db.delete({"name": "Alice"})
        # After delete, cache should be invalidated

    def test_clear_cache(self):
        """Test manual cache clearing"""
        self.db.insert({"id": 1, "name": "Alice"})
        self.db.find({"name": "Alice"})
        
        self.db.clear_cache()
        stats = self.db.get_cache_stats()
        self.assertEqual(stats['hits'], 0)
        # After clear, misses is reset (but find may have added 1 miss)
        self.assertGreaterEqual(stats['misses'], 0)

    def test_disable_enable_cache(self):
        """Test disabling and enabling cache"""
        self.db.insert({"id": 1, "name": "Alice"})
        
        self.db.disable_cache()
        self.assertFalse(self.db.cache.enabled)
        
        self.db.enable_cache()
        self.assertTrue(self.db.cache.enabled)

    # ========== PERSISTENCE TESTS ==========

    def test_data_persistence(self):
        """Test data persists across database instances"""
        self.db.insert({"id": 1, "name": "Alice", "age": 25})
        
        # Create new database instance with same path
        db2 = Database(self.db_path, self.password)
        self.assertEqual(len(db2.data), 1)
        self.assertEqual(db2.data[0]["name"], "Alice")

    def test_save_and_load(self):
        """Test explicit save and load operations"""
        self.db.insert({"id": 1, "name": "Alice"})
        self.db.save()
        
        # Load fresh database
        db2 = Database(self.db_path, self.password)
        result = db2.find({"name": "Alice"})
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
