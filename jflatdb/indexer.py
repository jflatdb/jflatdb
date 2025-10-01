"""
Indexing system
"""

class Indexer:
    def __init__(self):
        self.indexes = {}

    def build(self, data: list):
        self.indexes.clear()
        for record in data:
            for key, value in record.items():
                if key not in self.indexes:
                    self.indexes[key] = {}
                if value not in self.indexes[key]:
                    self.indexes[key][value] = []
                self.indexes[key][value].append(record)

    def query(self, data: list, conditions: dict):
        # For correctness and simplicity, filter directly against data using all conditions
        if not conditions:
            return data
        return [item for item in data if all(item.get(k) == v for k, v in conditions.items())]

