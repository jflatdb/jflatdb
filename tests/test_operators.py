"""
Test advanced query operators
"""

from jflatdb.database import Database

def main():
    db = Database("test_queries.json", password="test")

    # Clear any existing data
    db.data.clear()
    db.save()

    # Insert test data
    users = [
        {"id": 1, "name": "Alice", "age": 25, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 30, "city": "London"},
        {"id": 3, "name": "Charlie", "age": 20, "city": "Paris"},
        {"id": 4, "name": "Diana", "age": 35, "city": "Tokyo"},
        {"id": 5, "name": "Eve", "age": 28, "city": "Berlin"}
    ]

    for user in users:
        db.insert(user)

    print("All users:", db.find({}))

    # Test operators
    print("\n=== Testing Operators ===")

    # Greater than
    print("Age > 25:", db.find({"age": {"$gt": 25}}))

    # Less than or equal
    print("Age <= 30:", db.find({"age": {"$lte": 30}}))

    # Not equal
    print("Age != 25:", db.find({"age": {"$ne": 25}}))

    # IN
    print("ID in [1,3,5]:", db.find({"id": {"$in": [1, 3, 5]}}))

    # BETWEEN
    print("Age between 20 and 30:", db.find({"age": {"$between": [20, 30]}}))

    # LIKE
    print("Name like 'A%':", db.find({"name": {"$like": "A%"}}))
    print("Name like '%e%':", db.find({"name": {"$like": "%e%"}}))

    # Multiple conditions
    print("Age > 20 AND name like 'A%':", db.find({"age": {"$gt": 20}, "name": {"$like": "A%"}}))

if __name__ == "__main__":
    main()
