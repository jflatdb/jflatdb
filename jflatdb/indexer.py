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
        results = set()
        keys = list(conditions.keys())
        if not keys:
            return data

        # Try to use the index
        for key in keys:
            if key in self.indexes and conditions[key] in self.indexes[key]:
                found = self.indexes[key][conditions[key]]
                results.update(found)

        if not results:
            return [item for item in data if all(item.get(k) == v for k, v in conditions.items())]

        return list(results)

