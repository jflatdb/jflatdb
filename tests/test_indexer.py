import pytest
from jflatdb.indexer import Indexer  # Import Indexer from the package

# Sample dataset for testing
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Alice", "age": 25},
    {"name": "Charlie", "age": 30},
]

def test_build_store_full():
    """
    Test that build() stores full records when store_full=True
    """
    indexer = Indexer()
    indexer.build(data, store_full=True)
    
    # The stored items should be dicts (full records)
    assert isinstance(indexer.indexes["name"]["Alice"][0], dict)
    # Check that there are 2 records with age 30
    assert len(indexer.indexes["age"][30]) == 2

def test_build_store_indices():
    """
    Test that build() stores only indices when store_full=False
    """
    indexer = Indexer()
    indexer.build(data, store_full=False)
    
    # The stored items should be integers (indices)
    assert isinstance(indexer.indexes["name"]["Alice"][0], int)
    
    # Query using the index should return correct records
    results = indexer.query({"name": "Alice", "age": 25}, use_index=True)
    assert results == [{"name": "Alice", "age": 25}]

def test_query_without_index():
    """
    Test query() fallback when use_index=False
    """
    indexer = Indexer()
    indexer.build(data, store_full=False)
    
    results = indexer.query({"name": "Bob", "age": 25}, use_index=False)
    assert results == [{"name": "Bob", "age": 25}]

def test_query_missing_key():
    """
    Test query() when the key is missing in indexes
    """
    indexer = Indexer()
    indexer.build(data, store_full=False)
    
    results = indexer.query({"city": "NY"}, use_index=True)
    # Should fallback to scanning and return empty list
    assert results == []

def test_query_multiple_conditions():
    """
    Test query() with multiple conditions
    """
    indexer = Indexer()
    indexer.build(data, store_full=False)
    
    results = indexer.query({"name": "Alice", "age": 30}, use_index=True)
    assert results == [{"name": "Alice", "age": 30}]
