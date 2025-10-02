import pytest
from jflatdb.database import Database

@pytest.fixture
def db():
    db = Database("test_queries.json", password="test")
    db.data.clear()
    db.save()

    users = [
        {"id": 1, "name": "Alice", "age": 25, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 30, "city": "London"},
        {"id": 3, "name": "Charlie", "age": 20, "city": "Paris"},
        {"id": 4, "name": "Diana", "age": 35, "city": "Tokyo"},
        {"id": 5, "name": "Eve", "age": 28, "city": "Berlin"}
    ]

    for user in users:
        db.insert(user)

    return db

def test_find_all(db):
    results = db.find({})
    assert len(results) == 5

def test_gt_operator(db):
    results = db.find({"age": {"$gt": 25}})
    assert all(user["age"] > 25 for user in results)

def test_lte_operator(db):
    results = db.find({"age": {"$lte": 30}})
    assert all(user["age"] <= 30 for user in results)

def test_ne_operator(db):
    results = db.find({"age": {"$ne": 25}})
    assert all(user["age"] != 25 for user in results)

def test_in_operator(db):
    results = db.find({"id": {"$in": [1, 3, 5]}})
    assert {user["id"] for user in results} == {1, 3, 5}

def test_between_operator(db):
    results = db.find({"age": {"$between": [20, 30]}})
    assert all(20 <= user["age"] <= 30 for user in results)

def test_like_operator_prefix(db):
    results = db.find({"name": {"$like": "A%"}})
    assert all(user["name"].startswith("A") for user in results)

def test_like_operator_contains(db):
    results = db.find({"name": {"$like": "%e%"}})
    assert all("e" in user["name"] for user in results)

def test_combined_conditions(db):
    results = db.find({"age": {"$gt": 20}, "name": {"$like": "A%"}})
    assert all(user["age"] > 20 and user["name"].startswith("A") for user in results)
