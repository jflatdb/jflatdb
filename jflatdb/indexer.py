"""
Indexing system
"""
import re

class Indexer:
    def __init__(self):
        self.indexes = {}

    def build(self, data: list, store_full=False):
        """
        Build indexes for the dataset.

        Args:
            data (list): List of record dictionaries.
            store_full (bool): If True, store full records; if False, store only indices.
        """
        self.data = data  # Store original dataset
        self.indexes.clear()

        for idx, record in enumerate(data):
            for key, value in record.items():
                if key not in self.indexes:
                    self.indexes[key] = {}
                if value not in self.indexes[key]:
                    self.indexes[key][value] = []
                if store_full:
                    # Store full record (original behavior)
                    self.indexes[key][value].append(record)
                else:
                    # Store only index to save memory
                    self.indexes[key][value].append(idx)

    def query(self, conditions: dict, use_index=True):
        # For correctness and simplicity, filter directly against data using all conditions
        if not conditions:
            return self.data
        
        def matches_condition(item, key, value):
            item_value = item.get(key)
            if isinstance(value, dict):
                # Handle operator queries
             for op, op_value in value.items():
                    if item_value is None and op in ["$gt", "$lt", "$gte", "$lte", "$between"]:
                       return False
                    try:
                        if op == "$gt" and not (item_value > op_value):
                            return False
                        elif op == "$lt" and not (item_value < op_value):
                            return False
                        elif op == "$gte" and not (item_value >= op_value):
                            return False
                        elif op == "$lte" and not (item_value <= op_value):
                            return False
                        elif op == "$ne" and not (item_value != op_value):
                            return False
                        elif op == "$in" and item_value not in op_value:
                            return False
                        elif op == "$between":
                            if not isinstance(op_value, (list, tuple)) or len(op_value) != 2:
                                return False
                            if item_value is None or not (op_value[0] <= item_value <= op_value[1]):
                                return False
                        elif op == "$like":
                            if item_value is None:
                                return False
                            # SQL LIKE implementation: % for any chars, _ for single char
                            pattern = str(op_value).replace("%", ".*").replace("_", ".")
                            if not str(op_value).startswith("%"):
                                pattern = "^" + pattern
                            if not str(op_value).endswith("%"):
                                pattern = pattern + "$"
                            if not re.search(pattern, str(item_value), re.IGNORECASE):
                                return False
                    except (TypeError, ValueError):
                     return False
             return True
            else:
                # Simple equality
                return item_value == value
        
        return [item for item in self.data if all(matches_condition(item, k, v) for k, v in conditions.items())]
        
    