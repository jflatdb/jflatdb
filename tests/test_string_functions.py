import unittest
from jflatdb.query_engine import QueryEngine

class TestStringFunctions(unittest.TestCase):

    def setUp(self):
        self.data = [
            {'first_name': 'Akki', 'last_name': 'Kumar', 'city': 'Delhi', 'description': 'A nice person.', 'address': '  New Delhi  '},
            {'first_name': 'Sam', 'last_name': 'Gupta', 'city': 'Mumbai', 'description': 'Another nice person.', 'address': 'Mumbai'},
            {'first_name': 'Neha', 'last_name': 'Sharma', 'city': 'Pune', 'description': 'Yet another nice person.', 'address': '  Pune'},
            {'first_name': 'Test', 'last_name': None, 'city': 123, 'description': 'Test with non-string'}
        ]
        self.db = QueryEngine(self.data)

    def test_upper(self):
        self.assertEqual(self.db.upper('first_name'), ['AKKI', 'SAM', 'NEHA', 'TEST'])
        self.assertEqual(self.db.upper('city'), ['DELHI', 'MUMBAI', 'PUNE', None])

    def test_lower(self):
        self.assertEqual(self.db.lower('first_name'), ['akki', 'sam', 'neha', 'test'])
        self.assertEqual(self.db.lower('city'), ['delhi', 'mumbai', 'pune', None])

    def test_length(self):
        self.assertEqual(self.db.length('description'), [14, 20, 24, 20])
        self.assertEqual(self.db.length('last_name'), [5, 5, 6, None])

    def test_concat(self):
        self.assertEqual(self.db.concat('first_name', 'last_name'), ['AkkiKumar', 'SamGupta', 'NehaSharma', 'Test'])

    def test_trim(self):
        self.assertEqual(self.db.trim('address'), ['New Delhi', 'Mumbai', 'Pune', None])

if __name__ == '__main__':
    unittest.main()
