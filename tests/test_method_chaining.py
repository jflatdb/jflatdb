"""
Unit tests for method chaining functionality with QueryBuilder
"""
import os
import tempfile
import unittest
from jflatdb.database import Database


class TestMethodChaining(unittest.TestCase):
    """Test method chaining support in jflatdb"""

    def setUp(self):
        """Create temporary database for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_chaining.json")
        self.db = Database(self.db_path, password="test_password")

        # Insert test data
        self.test_data = [
            {"id": 1, "name": "Alice", "age": 30, "status": "active", "score": 85},
            {"id": 2, "name": "Bob", "age": 25, "status": "active", "score": 92},
            {"id": 3, "name": "Charlie", "age": 35, "status": "inactive", "score": 78},
            {"id": 4, "name": "David", "age": 28, "status": "active", "score": 88},
            {"id": 5, "name": "Eve", "age": 32, "status": "inactive", "score": 95},
        ]

        for record in self.test_data:
            self.db.insert(record)

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_basic_filter_fetch(self):
        """Test basic filter and fetch chain"""
        results = self.db.table("users").filter(status="active").fetch()
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertEqual(result["status"], "active")

    def test_filter_with_operators(self):
        """Test filter with operator-based queries"""
        results = self.db.table("users").filter(age__gt=30).fetch()
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertGreater(result["age"], 30)

    def test_filter_sort_chain(self):
        """Test filter followed by sort"""
        results = self.db.table("users").filter(status="active").sort("age").fetch()
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["name"], "Bob")
        self.assertEqual(results[1]["name"], "David")
        self.assertEqual(results[2]["name"], "Alice")

    def test_filter_sort_limit_chain(self):
        """Test filter, sort, and limit chain"""
        results = (
            self.db.table("users")
            .filter(status="active")
            .sort("age")
            .limit(2)
            .fetch()
        )
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "Bob")
        self.assertEqual(results[1]["name"], "David")

    def test_complete_chain(self):
        """Test complete chain: filter, sort, limit, fetch"""
        results = (
            self.db.table("users")
            .filter(age__gt=18)
            .sort("name")
            .limit(3)
            .fetch()
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["name"], "Alice")
        self.assertEqual(results[1]["name"], "Bob")
        self.assertEqual(results[2]["name"], "Charlie")

    def test_sort_reverse(self):
        """Test sorting in descending order"""
        results = self.db.table("users").sort("age", reverse=True).fetch()
        self.assertEqual(results[0]["name"], "Charlie")
        self.assertEqual(results[-1]["name"], "Bob")

    def test_limit_without_filter(self):
        """Test limit without filter"""
        results = self.db.table("users").limit(3).fetch()
        self.assertEqual(len(results), 3)

    def test_map_transformation(self):
        """Test map transformation on results"""
        results = (
            self.db.table("users")
            .filter(status="active")
            .map(lambda x: x["name"])
            .fetch()
        )
        self.assertEqual(len(results), 3)
        self.assertIn("Alice", results)
        self.assertIn("Bob", results)
        self.assertIn("David", results)

    def test_multiple_filters(self):
        """Test multiple filter calls"""
        results = (
            self.db.table("users")
            .filter(status="active")
            .filter(age__gt=26)
            .fetch()
        )
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result["status"], "active")
            self.assertGreater(result["age"], 26)

    def test_count_method(self):
        """Test count method on query chain"""
        count = self.db.table("users").filter(status="active").count()
        self.assertEqual(count, 3)

    def test_first_method(self):
        """Test first method returns single result"""
        result = self.db.table("users").filter(status="active").sort("age").first()
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Bob")

    def test_first_method_no_results(self):
        """Test first method returns None when no results"""
        result = self.db.table("users").filter(status="deleted").first()
        self.assertIsNone(result)

    def test_all_method(self):
        """Test all method as alias for fetch"""
        results = self.db.table("users").filter(status="active").all()
        self.assertEqual(len(results), 3)

    def test_complex_operators_chain(self):
        """Test complex operator combinations"""
        results = (
            self.db.table("users")
            .filter(age__gte=25, age__lte=32)
            .sort("score", reverse=True)
            .fetch()
        )
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Eve")
        self.assertEqual(results[1]["name"], "Bob")

    def test_between_operator(self):
        """Test between operator in filter"""
        results = self.db.table("users").filter(age__between=[25, 30]).fetch()
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertGreaterEqual(result["age"], 25)
            self.assertLessEqual(result["age"], 30)

    def test_in_operator(self):
        """Test in operator in filter"""
        results = (
            self.db.table("users")
            .filter(name__in=["Alice", "Bob", "Charlie"])
            .fetch()
        )
        self.assertEqual(len(results), 3)

    def test_ne_operator(self):
        """Test not equal operator"""
        results = self.db.table("users").filter(status__ne="inactive").fetch()
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertNotEqual(result["status"], "inactive")

    def test_empty_filter(self):
        """Test empty filter returns all results"""
        results = self.db.table("users").filter().fetch()
        self.assertEqual(len(results), 5)

    def test_chain_with_no_matches(self):
        """Test chain that results in no matches"""
        results = self.db.table("users").filter(age__gt=100).fetch()
        self.assertEqual(len(results), 0)

    def test_sort_with_missing_key(self):
        """Test sorting with missing key in some records"""
        self.db.insert({"id": 6, "name": "Frank", "status": "active"})
        results = self.db.table("users").sort("age").fetch()
        # Should still work, records without 'age' will have None as key
        self.assertIsNotNone(results)

    def test_map_with_complex_transformation(self):
        """Test map with complex transformation"""
        results = (
            self.db.table("users")
            .filter(status="active")
            .map(lambda x: {"name": x["name"], "score": x["score"]})
            .fetch()
        )
        self.assertEqual(len(results), 3)
        self.assertIn("name", results[0])
        self.assertIn("score", results[0])
        self.assertNotIn("age", results[0])

    def test_chaining_preserves_data_integrity(self):
        """Test that chaining doesn't modify original data"""
        original_count = len(self.db.data)
        _ = self.db.table("users").filter(status="active").sort("age").fetch()
        self.assertEqual(len(self.db.data), original_count)

    def test_multiple_chains_independent(self):
        """Test that multiple chains are independent"""
        chain1 = self.db.table("users").filter(status="active")
        chain2 = self.db.table("users").filter(status="inactive")

        results1 = chain1.fetch()
        results2 = chain2.fetch()

        self.assertEqual(len(results1), 3)
        self.assertEqual(len(results2), 2)

    def test_example_from_issue(self):
        """Test the exact example from the issue description"""
        # This is the proposed chained way from the issue
        final_data = (
            self.db.table("users")
            .filter(age__gt=18)
            .sort("name")
            .limit(10)
            .fetch()
        )
        self.assertIsNotNone(final_data)
        self.assertIsInstance(final_data, list)
        # All test data has age > 18, so we should get all 5 records (limited to 10)
        self.assertEqual(len(final_data), 5)
        # Should be sorted by name
        self.assertEqual(final_data[0]["name"], "Alice")


class TestMethodChainingEdgeCases(unittest.TestCase):
    """Test edge cases for method chaining"""

    def setUp(self):
        """Create temporary database for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_edge_cases.json")
        self.db = Database(self.db_path, password="test_password")

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_empty_database(self):
        """Test chaining on empty database"""
        results = self.db.table("empty").filter(status="active").fetch()
        self.assertEqual(len(results), 0)

    def test_limit_zero(self):
        """Test limit with zero"""
        self.db.insert({"id": 1, "name": "Test"})
        results = self.db.table("test").limit(0).fetch()
        self.assertEqual(len(results), 0)

    def test_limit_negative(self):
        """Test limit with negative number"""
        self.db.insert({"id": 1, "name": "Test"})
        results = self.db.table("test").limit(-1).fetch()
        # Negative limit should return empty list (Python slicing behavior)
        self.assertEqual(len(results), 0)

    def test_sort_mixed_types(self):
        """Test sorting with mixed types in column"""
        self.db.insert({"id": 1, "value": 10})
        self.db.insert({"id": 2, "value": "string"})
        self.db.insert({"id": 3, "value": 5})
        # Should not crash, might return unsorted
        results = self.db.table("test").sort("value").fetch()
        self.assertEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
