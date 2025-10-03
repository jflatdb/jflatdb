from jflatdb.query_engine import QueryEngine


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
