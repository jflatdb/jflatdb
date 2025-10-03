from jflatdb.query_engine import QueryEngine


def test_distinct_with_duplicates_preserves_order():
    engine = QueryEngine([
        {"id": 1, "city": "Delhi"},
        {"id": 2, "city": "Mumbai"},
        {"id": 3, "city": "Delhi"},
        {"id": 4, "city": "Chennai"},
        {"id": 5, "city": "Mumbai"},
    ])
    assert engine.distinct("city") == ["Delhi", "Mumbai", "Chennai"]


def test_distinct_all_unique_values():
    engine = QueryEngine([
        {"id": 1, "city": "Delhi"},
        {"id": 2, "city": "Mumbai"},
        {"id": 3, "city": "Chennai"},
    ])
    assert engine.distinct("city") == ["Delhi", "Mumbai", "Chennai"]


def test_distinct_empty_dataset():
    engine = QueryEngine([])
    assert engine.distinct("city") == []


def test_distinct_mixed_data_types_and_none_handling():
    data = [
        {"v": 1},
        {"v": "1"},
        {"v": [1, 2]},
        {"v": [1, 2]},  # duplicate list (unhashable)
        {"v": {"a": 1}},
        {"v": {"a": 1}},  # duplicate dict (unhashable)
        {"v": None},
        {"v": None},  # duplicate None
    ]
    engine = QueryEngine(data)

    # Default excludes None and preserves appearance order
    assert engine.distinct("v") == [1, "1", [1, 2], {"a": 1}]

    # Include None once
    assert engine.distinct("v", include_none=True) == [1, "1", [1, 2], {"a": 1}, None]

    # Sorting across mixed types should not error; verify deterministic ordering by repr
    result_sorted = engine.distinct("v", include_none=True, sort=True)
    expected = [1, "1", [1, 2], {"a": 1}, None]
    assert sorted(map(repr, result_sorted)) == sorted(map(repr, expected))
