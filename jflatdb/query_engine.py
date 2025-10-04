"""
In-Build Function(min,max,etc)
"""

from .exceptions.errors import QueryError


class QueryEngine:
    def __init__(self, table_data):
        self.data = table_data

    def min(self, column):
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        if not values:
            raise QueryError(f"Cannot compute min for column: {column} (empty dataset or no numeric values)")
        return min(values)

    def max(self, column):
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        if not values:
            raise QueryError(f"Cannot compute max for column: {column} (empty dataset or no numeric values)")
        return max(values)

    def avg(self, column):
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        if not values:
            raise QueryError(f"Cannot compute avg for column: {column} (empty dataset or no numeric values)")
        return sum(values) / len(values)

    def sum(self, column):
        values = [row[column] for row in self.data if column in row and isinstance(row[column], (int, float))]
        return sum(values) if values else 0

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

    def distinct(self, column, *, sort: bool = False, include_none: bool = False):
        """
        Return unique values from a column.

        Behavior:
        - Maintains order of first appearance by default.
        - Excludes None values by default (include with include_none=True).
        - Optionally sorts results using sort=True. If values are not mutually
          comparable (mixed types), falls back to sorting by repr to provide
          deterministic ordering.

        Args:
            column (str): Column name to extract unique values from.
            sort (bool): If True, return the unique values in sorted order.
            include_none (bool): If True, include None values if present.

        Returns:
            list: A list of unique values from the specified column.
        """
        try:
            results = []
            seen_hashable = set()

            for row in self.data:
                if column not in row:
                    continue
                value = row.get(column)
                if value is None and not include_none:
                    continue

                # Prefer O(1) membership for hashable values
                try:
                    is_hashable = True
                    _ = hash(value)
                except TypeError:
                    is_hashable = False

                if is_hashable:
                    if value not in seen_hashable:
                        seen_hashable.add(value)
                        results.append(value)
                else:
                    # Fallback: O(n) membership check for unhashable values (e.g., list, dict)
                    if not any(value == existing for existing in results):
                        results.append(value)

            if sort:
                try:
                    results = sorted(results)
                except TypeError:
                    # Mixed, non-comparable types; sort deterministically by representation
                    results = sorted(results, key=lambda v: repr(v))

            return results
        except Exception as exc:
            raise QueryError(f"Cannot compute distinct for column: {column}") from exc

    def upper(self, column):
        """Converts all string values in a column to uppercase."""
        try:
            result = []
            for row in self.data:
                value = row.get(column)
                if isinstance(value, str):
                    result.append(value.upper())
                else:
                    result.append(None)
            return result
        except Exception:
            raise QueryError(f"Cannot apply UPPER on column: {column}")

    def lower(self, column):
        """Converts all string values in a column to lowercase."""
        try:
            result = []
            for row in self.data:
                value = row.get(column)
                if isinstance(value, str):
                    result.append(value.lower())
                else:
                    result.append(None)
            return result
        except Exception:
            raise QueryError(f"Cannot apply LOWER on column: {column}")

    def length(self, column):
        """Returns the length of string values in a column."""
        try:
            result = []
            for row in self.data:
                value = row.get(column)
                if isinstance(value, str):
                    result.append(len(value))
                else:
                    result.append(None)
            return result
        except Exception:
            raise QueryError(f"Cannot compute LENGTH for column: {column}")

    def concat(self, *columns):
        """Combines multiple string columns into one."""
        if not columns:
            raise QueryError("CONCAT requires at least one column.")
        try:
            result = []
            for row in self.data:
                concatenated_str = ""
                for col in columns:
                    value = row.get(col)
                    if isinstance(value, str):
                        concatenated_str += value
                result.append(concatenated_str)
            return result
        except Exception:
            raise QueryError(f"Cannot CONCAT columns: {', '.join(columns)}")

    def trim(self, column):
        """Removes leading and trailing spaces from string values."""
        try:
            result = []
            for row in self.data:
                value = row.get(column)
                if isinstance(value, str):
                    result.append(value.strip())
                else:
                    result.append(None)
            return result
        except Exception:
            raise QueryError(f"Cannot apply TRIM on column: {column}")
