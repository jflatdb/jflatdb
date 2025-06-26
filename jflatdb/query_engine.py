"""
In-Build Function(min,max,etc)
"""

from .exceptions.errors import QueryError

class QueryEngine:
    def __init__(self, table_data):
        self.data = table_data

    def min(self, column):
        try:
            values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
            return min(values) if values else None
        except Exception:
            raise QueryError(f"Cannot compute min for column: {column}")

    def max(self, column):
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        return max(values) if values else None

    def avg(self, column):
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        return sum(values) / len(values) if values else None

    def count(self, column=None):
        if column:
            return sum(1 for row in self.data if column in row and row[column] is not None)
        return len(self.data)

    def between(self, column, low, high):
        return [row for row in self.data if column in row and low <= row[column] <= high]

    def group_by(self, column):
        grouped = {}
        for row in self.data:
            key = row.get(column)
            if key is not None:
                grouped.setdefault(key, []).append(row)
        return grouped
