# Method Chaining in jflatdb

## Overview

Method chaining provides a fluent, expressive way to build and execute database queries in jflatdb. Instead of writing multiple separate statements, you can chain operations together in a single, readable expression.

## Why Method Chaining?

### Before (Traditional Approach)
```python
results = db.find({"age": {"$gt": 18}})
results = sorted(results, key=lambda x: x.get("name"))
results = results[:10]
```

### After (Method Chaining)
```python
results = db.table("users").filter(age__gt=18).sort("name").limit(10).fetch()
```

Method chaining is:
- **More readable**: Operations flow naturally from left to right
- **More intuitive**: Resembles SQL and other query languages
- **More maintainable**: Easy to add, remove, or reorder operations
- **Lazy evaluation**: Operations execute only when you call a terminal method like `fetch()`

## Getting Started

### Basic Usage

```python
from jflatdb.database import Database

db = Database("users.json", password="your-password")

# Insert sample data
db.insert({"id": 1, "name": "Alice", "age": 30, "status": "active"})
db.insert({"id": 2, "name": "Bob", "age": 25, "status": "active"})
db.insert({"id": 3, "name": "Charlie", "age": 35, "status": "inactive"})

# Simple chained query
results = db.table("users").filter(status="active").fetch()
```

## Available Methods

### Chainable Methods

These methods return a `QueryBuilder` instance, allowing you to chain more operations:

#### `table(name="default")`
Creates a new QueryBuilder instance for chaining operations.

```python
query = db.table("users")
```

#### `filter(**kwargs)`
Filters records based on conditions. Supports both simple equality and operator-based queries.

**Simple equality:**
```python
db.table("users").filter(status="active").fetch()
```

**Operator-based queries:**
```python
# Greater than
db.table("users").filter(age__gt=25).fetch()

# Less than
db.table("users").filter(age__lt=30).fetch()

# Greater than or equal
db.table("users").filter(age__gte=25).fetch()

# Less than or equal
db.table("users").filter(age__lte=30).fetch()

# Not equal
db.table("users").filter(status__ne="inactive").fetch()

# In list
db.table("users").filter(name__in=["Alice", "Bob"]).fetch()

# Between range
db.table("users").filter(age__between=[25, 35]).fetch()

# Pattern matching (SQL LIKE)
db.table("users").filter(name__like="A%").fetch()
```

**Multiple conditions:**
```python
# Multiple conditions in one filter
db.table("users").filter(status="active", age__gt=25).fetch()

# Multiple filter calls (chained)
db.table("users").filter(status="active").filter(age__gt=25).fetch()
```

#### `sort(key, reverse=False)`
Sorts results by a specified field.

```python
# Ascending order
db.table("users").sort("name").fetch()

# Descending order
db.table("users").sort("age", reverse=True).fetch()
```

#### `limit(count)`
Limits the number of results returned.

```python
# Get first 10 results
db.table("users").limit(10).fetch()

# Combine with filter and sort
db.table("users").filter(status="active").sort("name").limit(5).fetch()
```

#### `map(func)`
Applies a transformation function to each result.

```python
# Extract just names
names = db.table("users").filter(status="active").map(lambda x: x["name"]).fetch()

# Transform to custom format
users = db.table("users").map(lambda x: {
    "id": x["id"],
    "full_name": x["name"].upper()
}).fetch()
```

### Terminal Methods

These methods execute the query and return results:

#### `fetch()`
Executes the query chain and returns all matching results as a list.

```python
results = db.table("users").filter(status="active").fetch()
# Returns: [{"id": 1, "name": "Alice", ...}, ...]
```

#### `all()`
Alias for `fetch()`. Returns all matching results.

```python
results = db.table("users").filter(status="active").all()
```

#### `count()`
Returns the number of matching records without fetching them.

```python
count = db.table("users").filter(status="active").count()
# Returns: 2
```

#### `first()`
Returns the first matching record, or `None` if no results.

```python
user = db.table("users").filter(status="active").sort("age").first()
# Returns: {"id": 2, "name": "Bob", ...} or None
```

## Complete Examples

### Example 1: Filter, Sort, and Limit

```python
from jflatdb.database import Database

db = Database("products.json", password="secret")

# Get top 5 expensive products in Electronics category
top_products = (
    db.table("products")
    .filter(category="Electronics", in_stock=True)
    .sort("price", reverse=True)
    .limit(5)
    .fetch()
)
```

### Example 2: Complex Filtering

```python
# Find users aged 25-35 who are active
users = (
    db.table("users")
    .filter(age__gte=25, age__lte=35)
    .filter(status="active")
    .sort("name")
    .fetch()
)

# Alternative using between
users = (
    db.table("users")
    .filter(age__between=[25, 35], status="active")
    .sort("name")
    .fetch()
)
```

### Example 3: Data Transformation

```python
# Get list of active user names in uppercase
names = (
    db.table("users")
    .filter(status="active")
    .sort("name")
    .map(lambda x: x["name"].upper())
    .fetch()
)
# Returns: ["ALICE", "BOB"]
```

### Example 4: Pattern Matching

```python
# Find all users whose names start with 'A'
users = db.table("users").filter(name__like="A%").fetch()

# Find all users whose names contain 'bob'
users = db.table("users").filter(name__like="%bob%").fetch()

# Find all users whose names end with 'son'
users = db.table("users").filter(name__like="%son").fetch()
```

### Example 5: Count and First

```python
# Count active users
active_count = db.table("users").filter(status="active").count()
print(f"Active users: {active_count}")

# Get the youngest active user
youngest = (
    db.table("users")
    .filter(status="active")
    .sort("age")
    .first()
)

if youngest:
    print(f"Youngest: {youngest['name']}, Age: {youngest['age']}")
```

### Example 6: Multiple Independent Chains

```python
# Create independent query chains
active_users = db.table("users").filter(status="active")
inactive_users = db.table("users").filter(status="inactive")

# Execute them separately
active_list = active_users.fetch()
inactive_list = inactive_users.fetch()

print(f"Active: {len(active_list)}, Inactive: {len(inactive_list)}")
```

## Supported Operators

| Operator | Syntax | Description | Example |
|----------|--------|-------------|---------|
| Equal | `field=value` | Exact match | `filter(status="active")` |
| Greater than | `field__gt=value` | Greater than | `filter(age__gt=25)` |
| Less than | `field__lt=value` | Less than | `filter(age__lt=30)` |
| Greater or equal | `field__gte=value` | Greater than or equal | `filter(age__gte=25)` |
| Less or equal | `field__lte=value` | Less than or equal | `filter(age__lte=30)` |
| Not equal | `field__ne=value` | Not equal | `filter(status__ne="deleted")` |
| In | `field__in=[values]` | Value in list | `filter(id__in=[1,2,3])` |
| Between | `field__between=[low, high]` | Value in range | `filter(age__between=[25, 35])` |
| Like | `field__like="pattern"` | Pattern matching | `filter(name__like="A%")` |

## Best Practices

### 1. Use Descriptive Table Names
```python
# Good
users_query = db.table("users")
products_query = db.table("products")

# Acceptable (default)
query = db.table()
```

### 2. Chain Operations in Logical Order
```python
# Good: filter -> sort -> limit -> fetch
results = (
    db.table("users")
    .filter(status="active")
    .sort("name")
    .limit(10)
    .fetch()
)
```

### 3. Use Multiple Filters for Complex Conditions
```python
# Clear and readable
results = (
    db.table("users")
    .filter(status="active")
    .filter(age__gte=18, age__lte=65)
    .filter(country="USA")
    .fetch()
)
```

### 4. Check Results Before Processing
```python
# Use first() for single results
user = db.table("users").filter(email="user@example.com").first()
if user:
    print(f"Found user: {user['name']}")
else:
    print("User not found")
```

### 5. Use count() for Existence Checks
```python
# Efficient way to check if records exist
if db.table("users").filter(email="user@example.com").count() > 0:
    print("User exists")
```

## Performance Considerations

1. **Lazy Evaluation**: Operations are not executed until a terminal method (`fetch()`, `count()`, `first()`, `all()`) is called.

2. **Filter Early**: Apply filters before sorting to reduce the dataset size.
   ```python
   # Good
   db.table("users").filter(status="active").sort("name").fetch()

   # Less efficient
   db.table("users").sort("name").filter(status="active").fetch()
   ```

3. **Use limit()**: When you only need a few results, use `limit()` to avoid processing the entire dataset.

4. **Sequential Filters**: Multiple filter calls are applied sequentially, allowing for complex filtering logic.

## Migration from Traditional API

### Before
```python
# Find with operators
users = db.find({"age": {"$gt": 25}, "status": "active"})

# Manual sorting
users = sorted(users, key=lambda x: x.get("name"))

# Manual limiting
users = users[:10]
```

### After
```python
# Method chaining
users = (
    db.table("users")
    .filter(age__gt=25, status="active")
    .sort("name")
    .limit(10)
    .fetch()
)
```

**Note**: The traditional API (`db.find()`, `db.insert()`, etc.) still works and is fully supported. Method chaining is an additional feature for more expressive queries.

## Common Patterns

### Pagination
```python
page = 1
page_size = 10
offset = (page - 1) * page_size

# Get total count
total = db.table("users").filter(status="active").count()

# Get page results
results = (
    db.table("users")
    .filter(status="active")
    .sort("created_at", reverse=True)
    .fetch()
)[offset:offset + page_size]
```

### Search with Multiple Criteria
```python
def search_users(name_pattern, min_age, max_age, status):
    query = db.table("users")

    if name_pattern:
        query = query.filter(name__like=f"%{name_pattern}%")
    if min_age:
        query = query.filter(age__gte=min_age)
    if max_age:
        query = query.filter(age__lte=max_age)
    if status:
        query = query.filter(status=status)

    return query.fetch()
```

### Aggregation with map()
```python
# Get average age of active users
active_ages = (
    db.table("users")
    .filter(status="active")
    .map(lambda x: x["age"])
    .fetch()
)
average_age = sum(active_ages) / len(active_ages) if active_ages else 0
```

## Error Handling

```python
try:
    results = (
        db.table("users")
        .filter(age__gt=18)
        .sort("name")
        .fetch()
    )
except Exception as e:
    print(f"Query failed: {e}")
```

## Summary

Method chaining in jflatdb provides:
- ✅ Fluent, readable query syntax
- ✅ Support for complex filtering with operators
- ✅ Lazy evaluation for better performance
- ✅ Chainable operations: `filter()`, `sort()`, `limit()`, `map()`
- ✅ Terminal methods: `fetch()`, `all()`, `count()`, `first()`
- ✅ Full compatibility with existing jflatdb API

Start using method chaining today to write cleaner, more expressive database queries!
