from jflatdb.query_engine import QueryEngine
import pytest
from jflatdb.exceptions.errors import QueryError


class TestSumFunction:
    """Test suite for QueryEngine.sum() method"""

    def test_sum_normal_numeric_data(self):
        """Test sum with normal numeric integer data"""
        engine = QueryEngine([
            {"id": 1, "salary": 3000},
            {"id": 2, "salary": 4000},
            {"id": 3, "salary": 2500},
        ])
        assert engine.sum("salary") == 9500

    def test_sum_float_data(self):
        """Test sum with float values"""
        engine = QueryEngine([
            {"id": 1, "price": 10.5},
            {"id": 2, "price": 20.75},
            {"id": 3, "price": 15.25},
        ])
        assert engine.sum("price") == 46.5

    def test_sum_mixed_int_float(self):
        """Test sum with mixed int and float values"""
        engine = QueryEngine([
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 50.5},
            {"id": 3, "amount": 25},
        ])
        assert engine.sum("amount") == 175.5

    def test_sum_empty_dataset(self):
        """Test sum with empty dataset returns 0"""
        engine = QueryEngine([])
        assert engine.sum("salary") == 0

    def test_sum_column_not_present(self):
        """Test sum when column doesn't exist in any row returns 0"""
        engine = QueryEngine([
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ])
        assert engine.sum("salary") == 0

    def test_sum_non_numeric_values(self):
        """Test sum ignores non-numeric values"""
        engine = QueryEngine([
            {"id": 1, "value": 100},
            {"id": 2, "value": "not a number"},
            {"id": 3, "value": 200},
            {"id": 4, "value": None},
            {"id": 5, "value": 50},
        ])
        assert engine.sum("value") == 350

    def test_sum_all_non_numeric(self):
        """Test sum with all non-numeric values returns 0"""
        engine = QueryEngine([
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ])
        assert engine.sum("name") == 0

    def test_sum_partial_column_presence(self):
        """Test sum when column is present in some rows only"""
        engine = QueryEngine([
            {"id": 1, "salary": 3000},
            {"id": 2, "name": "Bob"},
            {"id": 3, "salary": 2500},
        ])
        assert engine.sum("salary") == 5500

    def test_sum_negative_values(self):
        """Test sum with negative values"""
        engine = QueryEngine([
            {"id": 1, "balance": 100},
            {"id": 2, "balance": -50},
            {"id": 3, "balance": 75},
            {"id": 4, "balance": -25},
        ])
        assert engine.sum("balance") == 100

    def test_sum_zero_values(self):
        """Test sum with zero values"""
        engine = QueryEngine([
            {"id": 1, "score": 0},
            {"id": 2, "score": 0},
            {"id": 3, "score": 0},
        ])
        assert engine.sum("score") == 0

    def test_sum_single_value(self):
        """Test sum with single value"""
        engine = QueryEngine([
            {"id": 1, "amount": 42},
        ])
        assert engine.sum("amount") == 42


class TestMinMaxAvgFunctions:
    """Test suite for QueryEngine min(), max(), and avg() methods"""

    def test_min_normal(self):
        engine = QueryEngine([{"val": 10}, {"val": 5}, {"val": 20}])
        assert engine.min("val") == 5

    def test_max_normal(self):
        engine = QueryEngine([{"val": 10}, {"val": 5}, {"val": 20}])
        assert engine.max("val") == 20

    def test_avg_normal(self):
        engine = QueryEngine([{"val": 10}, {"val": 5}, {"val": 15}])
        assert engine.avg("val") == 10

    def test_empty_dataset_raises_error(self):
        engine = QueryEngine([])
        with pytest.raises(QueryError, match="Cannot compute min for column: val"):
            engine.min("val")
        with pytest.raises(QueryError, match="Cannot compute max for column: val"):
            engine.max("val")
        with pytest.raises(QueryError, match="Cannot compute avg for column: val"):
            engine.avg("val")

    def test_no_numeric_values_raises_error(self):
        engine = QueryEngine([{"val": "a"}, {"val": "b"}])
        with pytest.raises(QueryError):
            engine.min("val")
        with pytest.raises(QueryError):
            engine.max("val")
        with pytest.raises(QueryError):
            engine.avg("val")

    def test_mixed_values(self):
        engine = QueryEngine([{"val": 10}, {"val": "a"}, {"val": 20}])
        assert engine.min("val") == 10
        assert engine.max("val") == 20
        assert engine.avg("val") == 15


class TestCountFunction:
    """Test suite for QueryEngine.count() method"""

    def test_count_empty_dataset(self):
        engine = QueryEngine([])
        assert engine.count() == 0
        assert engine.count("any_column") == 0

    def test_count_all(self):
        engine = QueryEngine([{"a": 1}, {"a": 2}, {}])
        assert engine.count() == 3

    def test_count_column(self):
        engine = QueryEngine([{"a": 1}, {"a": None}, {"b": 3}])
        assert engine.count("a") == 1


class TestBetweenFunction:
    """Test suite for QueryEngine.between() method"""

    def test_between_empty_dataset(self):
        engine = QueryEngine([])
        assert engine.between("age", 18, 30) == []

    def test_between_normal(self):
        engine = QueryEngine([
            {"age": 25},
            {"age": 17},
            {"age": 35},
            {"age": 30}
        ])
        assert engine.between("age", 18, 30) == [{"age": 25}, {"age": 30}]


class TestGroupByFunction:
    """Test suite for QueryEngine.group_by() method"""

    def test_group_by_empty_dataset(self):
        engine = QueryEngine([])
        assert engine.group_by("category") == {}

    def test_group_by_normal(self):
        engine = QueryEngine([
            {"category": "A", "value": 1},
            {"category": "B", "value": 2},
            {"category": "A", "value": 3},
        ])
        expected = {
            "A": [{"category": "A", "value": 1}, {"category": "A", "value": 3}],
            "B": [{"category": "B", "value": 2}]
        }
        assert engine.group_by("category") == expected
