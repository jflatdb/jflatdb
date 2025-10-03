# Query Engine Documentation

## Overview

The **QueryEngine** provides SQL-like aggregate functions and advanced query operations for in-memory data analysis. It works with lists of dictionaries (JSON-like data structures) and offers a simple, Pythonic API.

---

## Getting Started

```python
from jflatdb.query_engine import QueryEngine

# Sample data
data = [
    {"id": 1, "name": "Alice", "salary": 3000, "department": "Engineering"},
    {"id": 2, "name": "Bob", "salary": 4000, "department": "Sales"},
    {"id": 3, "name": "Charlie", "salary": 2500, "department": "Engineering"},
    {"id": 4, "name": "Diana", "salary": 3500, "department": "Sales"}
]

# Initialize QueryEngine
engine = QueryEngine(data)
```

---

## Aggregate Functions

### `sum(column)`

Calculates the total sum of numeric values in a column.

**Parameters:**
- `column` (str): The column name to sum

**Returns:**
- `int` or `float`: Sum of all numeric values
- `0`: If no numeric values found or empty dataset

**Behavior:**
- Only numeric values (`int`, `float`) are included
- Non-numeric values are automatically ignored
- Missing columns are handled gracefully

**Examples:**

```python
# Basic sum
total_salary = engine.sum("salary")
# Output: 13000

# Empty dataset
empty_engine = QueryEngine([])
result = empty_engine.sum("salary")
# Output: 0

# Mixed numeric/non-numeric values
data_with_nulls = [
    {"id": 1, "value": 100},
    {"id": 2, "value": "invalid"},
    {"id": 3, "value": 200},
    {"id": 4, "value": None}
]
engine = QueryEngine(data_with_nulls)
total = engine.sum("value")
# Output: 300 (ignores "invalid" and None)
```

---

### `avg(column)`

Calculates the average (mean) of numeric values in a column.

**Parameters:**
- `column` (str): The column name to average

**Returns:**
- `float`: Average of numeric values
- `None`: If no numeric values found or empty dataset

**Examples:**

```python
# Calculate average salary
avg_salary = engine.avg("salary")
# Output: 3250.0

# No numeric values
result = engine.avg("name")
# Output: None
```

---

### `min(column)`

Finds the minimum value in a column.

**Parameters:**
- `column` (str): The column name

**Returns:**
- `int` or `float`: Minimum numeric value
- `None`: If no numeric values found or empty dataset

**Examples:**

```python
# Find minimum salary
min_salary = engine.min("salary")
# Output: 2500
```

---

### `max(column)`

Finds the maximum value in a column.

**Parameters:**
- `column` (str): The column name

**Returns:**
- `int` or `float`: Maximum numeric value
- `None`: If no numeric values found or empty dataset

**Examples:**

```python
# Find maximum salary
max_salary = engine.max("salary")
# Output: 4000
```

---

### `count(column=None)`

Counts records or non-null values in a column.

**Parameters:**
- `column` (str, optional): Column name to count. If `None`, counts all records.

**Returns:**
- `int`: Count of records or non-null values

**Examples:**

```python
# Count all records
total_records = engine.count()
# Output: 4

# Count non-null values in a column
salary_count = engine.count("salary")
# Output: 4

# Count with missing values
data_with_nulls = [
    {"id": 1, "email": "alice@example.com"},
    {"id": 2, "email": None},
    {"id": 3, "email": "charlie@example.com"}
]
engine = QueryEngine(data_with_nulls)
email_count = engine.count("email")
# Output: 2 (excludes None)
```

---

## Filter and Group Operations

### `between(column, low, high)`

Filters records where column value is between low and high (inclusive).

**Parameters:**
- `column` (str): Column name
- `low` (int/float): Lower bound (inclusive)
- `high` (int/float): Upper bound (inclusive)

**Returns:**
- `list`: Records matching the criteria

**Examples:**

```python
# Find salaries between 3000 and 3500
mid_range = engine.between("salary", 3000, 3500)
# Output: [
#     {"id": 1, "name": "Alice", "salary": 3000, "department": "Engineering"},
#     {"id": 4, "name": "Diana", "salary": 3500, "department": "Sales"}
# ]
```

---

### `group_by(column)`

Groups records by unique values in a column.

**Parameters:**
- `column` (str): Column name to group by

**Returns:**
- `dict`: Dictionary where keys are unique column values and values are lists of records

**Examples:**

```python
# Group employees by department
grouped = engine.group_by("department")
# Output: {
#     "Engineering": [
#         {"id": 1, "name": "Alice", "salary": 3000, "department": "Engineering"},
#         {"id": 3, "name": "Charlie", "salary": 2500, "department": "Engineering"}
#     ],
#     "Sales": [
#         {"id": 2, "name": "Bob", "salary": 4000, "department": "Sales"},
#         {"id": 4, "name": "Diana", "salary": 3500, "department": "Sales"}
#     ]
# }
```

---

### `distinct(column, *, sort=False, include_none=False)`

Returns unique values from a column.

Parameters:
- `column` (str): Column name to extract values from
- `sort` (bool, default False): If True, sort the result. For mixed, non-comparable
    types, a deterministic sort by representation is used.
- `include_none` (bool, default False): If True, include `None` values in the output.

Returns:
- `list`: Unique values, preserving the first-seen order by default.

Behavior:
- By default, order of appearance is maintained.
- `None` values are excluded by default; enable with `include_none=True`.
- Handles both hashable and unhashable values (e.g., lists, dicts).

Examples:

```python
engine = QueryEngine([
        {"id": 1, "city": "Delhi"},
        {"id": 2, "city": "Mumbai"},
        {"id": 3, "city": "Delhi"},
        {"id": 4, "city": "Chennai"},
])

engine.distinct("city")
# ["Delhi", "Mumbai", "Chennai"]

# Include None and sort
engine2 = QueryEngine([{"v": None}, {"v": 2}, {"v": 1}, {"v": None}])
engine2.distinct("v", include_none=True, sort=True)
# Deterministically sorted list including None: [1, 2, None]
```

---

## Combining Operations

QueryEngine operations can be combined for complex analysis:

```python
# Calculate average salary by department
grouped = engine.group_by("department")
for dept, employees in grouped.items():
    dept_engine = QueryEngine(employees)
    avg_sal = dept_engine.avg("salary")
    print(f"{dept}: ${avg_sal:.2f}")
# Output:
# Engineering: $2750.00
# Sales: $3750.00

# Find total salary for high earners (>3000)
high_earners = engine.between("salary", 3001, 10000)
high_earner_engine = QueryEngine(high_earners)
total = high_earner_engine.sum("salary")
# Output: 7500
```

---

## Error Handling

QueryEngine methods handle edge cases gracefully:

```python
# Non-existent column
result = engine.sum("nonexistent")
# Output: 0

# Empty dataset
empty = QueryEngine([])
result = empty.avg("salary")
# Output: None

# All non-numeric values
text_data = [{"name": "Alice"}, {"name": "Bob"}]
engine = QueryEngine(text_data)
result = engine.sum("name")
# Output: 0
```

---

## Best Practices

1. **Data Validation**: Ensure your data is in list-of-dicts format
2. **Column Names**: Use consistent column naming across records
3. **Type Consistency**: While QueryEngine handles mixed types, consistent types improve performance
4. **Memory Usage**: QueryEngine works in-memory; consider data size for large datasets
