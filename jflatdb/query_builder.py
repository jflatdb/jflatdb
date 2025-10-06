"""
QueryBuilder class for method chaining support
"""


class QueryBuilder:
    """
    A chainable query builder for database operations.

    Supports method chaining for filter, sort, limit, and map operations.
    All operations are lazy and executed only when fetch() is called.

    Example:
        results = db.table("users").filter(age__gt=18).sort("name").limit(10).fetch()
    """

    def __init__(self, database, table_name):
        """
        Initialize QueryBuilder with database instance and table name.

        Args:
            database: The Database instance
            table_name: Name of the table (used for logging/debugging)
        """
        self.database = database
        self.table_name = table_name
        self._data = database.data
        self._filter_conditions = []
        self._sort_key = None
        self._sort_reverse = False
        self._limit_count = None
        self._map_function = None

    def filter(self, **kwargs):
        """
        Add filter conditions to the query chain.

        Supports operator-based queries using double underscore notation:
        - age__gt=18 (greater than)
        - age__lt=30 (less than)
        - age__gte=18 (greater than or equal)
        - age__lte=30 (less than or equal)
        - age__ne=25 (not equal)
        - name__in=["Alice", "Bob"] (in list)
        - age__between=[18, 30] (between range)
        - name__like="%John%" (pattern matching)

        Args:
            **kwargs: Filter conditions

        Returns:
            QueryBuilder: Self for chaining

        Example:
            db.table("users").filter(age__gt=18, status="active")
        """
        if kwargs:
            # Convert kwargs to indexer-compatible query format
            query = {}
            for key, value in kwargs.items():
                if "__" in key:
                    # Handle operator-based queries
                    field, operator = key.rsplit("__", 1)
                    op_map = {
                        "gt": "$gt",
                        "lt": "$lt",
                        "gte": "$gte",
                        "lte": "$lte",
                        "ne": "$ne",
                        "in": "$in",
                        "between": "$between",
                        "like": "$like"
                    }
                    if operator in op_map:
                        if field not in query:
                            query[field] = {}
                        if isinstance(query[field], dict):
                            query[field][op_map[operator]] = value
                        else:
                            # Field already has a simple value, convert to operator dict
                            old_value = query[field]
                            query[field] = {"$eq": old_value, op_map[operator]: value}
                    else:
                        # Not a recognized operator, treat as regular field
                        query[key] = value
                else:
                    # Simple equality
                    query[key] = value

            self._filter_conditions.append(query)

        return self

    def sort(self, key, reverse=False):
        """
        Add sorting to the query chain.

        Args:
            key: Field name to sort by
            reverse: If True, sort in descending order (default: False)

        Returns:
            QueryBuilder: Self for chaining

        Example:
            db.table("users").sort("name")
            db.table("users").sort("age", reverse=True)
        """
        self._sort_key = key
        self._sort_reverse = reverse
        return self

    def limit(self, count):
        """
        Limit the number of results returned.

        Args:
            count: Maximum number of results to return

        Returns:
            QueryBuilder: Self for chaining

        Example:
            db.table("users").limit(10)
        """
        self._limit_count = count
        return self

    def map(self, func):
        """
        Apply a transformation function to each result.

        Args:
            func: Function to apply to each record

        Returns:
            QueryBuilder: Self for chaining

        Example:
            db.table("users").map(lambda x: x["name"])
        """
        self._map_function = func
        return self

    def fetch(self):
        """
        Execute the query chain and return results.

        This is the terminal operation that executes all chained operations
        in order: filter -> sort -> limit -> map

        Returns:
            list: Query results

        Example:
            results = db.table("users").filter(age__gt=18).fetch()
        """
        # Start with all data
        results = self._data

        # Apply filters
        for filter_query in self._filter_conditions:
            if filter_query:
                results = self.database.indexer.query(filter_query)

        # Apply sorting
        if self._sort_key:
            try:
                results = sorted(
                    results,
                    key=lambda x: x.get(self._sort_key),
                    reverse=self._sort_reverse
                )
            except (TypeError, KeyError):
                # If sorting fails, return unsorted results
                pass

        # Apply limit
        if self._limit_count is not None:
            results = results[:self._limit_count]

        # Apply map transformation
        if self._map_function:
            results = [self._map_function(item) for item in results]

        return results

    def count(self):
        """
        Count the number of results without fetching them.

        Returns:
            int: Number of matching records

        Example:
            count = db.table("users").filter(age__gt=18).count()
        """
        # Execute filters but not map
        results = self._data

        for filter_query in self._filter_conditions:
            if filter_query:
                results = self.database.indexer.query(filter_query)

        return len(results)

    def first(self):
        """
        Get the first result from the query.

        Returns:
            dict or None: First matching record or None if no results

        Example:
            user = db.table("users").filter(status="active").first()
        """
        results = self.limit(1).fetch()
        return results[0] if results else None

    def all(self):
        """
        Alias for fetch() - returns all matching results.

        Returns:
            list: Query results

        Example:
            users = db.table("users").filter(age__gt=18).all()
        """
        return self.fetch()
