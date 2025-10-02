"""
Demo: Query Caching Performance
This script demonstrates the performance benefits of query caching in jflatdb
"""

import time
from jflatdb.database import Database

# Initialize database with caching enabled
print("=== Query Caching Demo ===\n")

db = Database("cache_demo.json", password="demo123", cache_size=100)

# Insert sample data
print("Inserting 100 sample records...")
for i in range(100):
    db.insert({
        "id": i,
        "name": f"User_{i}",
        "age": 20 + (i % 30),
        "status": "active" if i % 2 == 0 else "inactive"
    })
print("✓ Data inserted\n")

# Demo 1: Cache Miss vs Cache Hit
print("--- Demo 1: Cache Miss vs Cache Hit ---")

# First query (cache miss)
start = time.time()
result1 = db.find({"status": "active"})
time1 = time.time() - start
print(
    f"First query (cache miss): {time1*1000:.2f}ms - "
    f"Found {len(result1)} records"
)

# Same query (cache hit)
start = time.time()
result2 = db.find({"status": "active"})
time2 = time.time() - start
print(
    f"Second query (cache hit): {time2*1000:.2f}ms - "
    f"Found {len(result2)} records"
)

speedup = time1 / time2 if time2 > 0 else float('inf')
print(f"Speedup: {speedup:.1f}x faster\n")

# Demo 2: Cache Statistics
print("--- Demo 2: Cache Statistics ---")

# Execute various queries
db.find({"age": {"$gt": 25}})
db.find({"age": {"$gt": 25}})  # Hit
db.find({"status": "inactive"})
db.find({"status": "inactive"})  # Hit
db.find({"age": {"$between": [20, 30]}})

stats = db.get_cache_stats()
print(f"Cache enabled: {stats['enabled']}")
print(f"Cache size: {stats['size']}/{stats['max_size']}")
print(f"Cache hits: {stats['hits']}")
print(f"Cache misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate']}\n")

# Demo 3: Cache Invalidation
print("--- Demo 3: Cache Invalidation ---")

# Query to populate cache
db.find({"name": "User_1"})
print(f"Before insert - Cache size: {db.get_cache_stats()['size']}")

# Insert invalidates cache
db.insert({"id": 200, "name": "New_User", "age": 25, "status": "active"})
print(
    f"After insert - Cache size: {db.get_cache_stats()['size']} "
    "(cache cleared)"
)

# Query again
db.find({"name": "User_1"})
print(f"After query - Cache size: {db.get_cache_stats()['size']}\n")

# Demo 4: Repeated Queries Performance
print("--- Demo 4: Repeated Queries (1000x) ---")

query = {"age": {"$gt": 30}}

# First run (will use cache after first query)
start = time.time()
for _ in range(1000):
    db.find(query)
time_with_cache = time.time() - start
print(f"With cache: {time_with_cache*1000:.2f}ms for 1000 queries")

# Disable cache and run again
db.disable_cache()
start = time.time()
for _ in range(1000):
    db.find(query)
time_without_cache = time.time() - start
print(f"Without cache: {time_without_cache*1000:.2f}ms for 1000 queries")

speedup = (
    time_without_cache / time_with_cache
    if time_with_cache > 0
    else float('inf')
)
print(f"Speedup: {speedup:.1f}x faster with caching\n")

# Re-enable cache
db.enable_cache()

# Demo 5: LRU Eviction
print("--- Demo 5: LRU Eviction ---")

# Create db with small cache
small_cache_db = Database("lru_demo.json", password="demo", cache_size=3)

for i in range(5):
    small_cache_db.insert({"id": i, "value": i * 10})

# Fill cache
small_cache_db.find({"id": 1})
small_cache_db.find({"id": 2})
small_cache_db.find({"id": 3})
print(
    f"Cache size after 3 queries: "
    f"{small_cache_db.get_cache_stats()['size']}"
)

# Access id=1 (moves to most recent)
small_cache_db.find({"id": 1})

# Add new query (should evict id=2, the least recent)
small_cache_db.find({"id": 4})
print(
    f"Cache size after 4th query: "
    f"{small_cache_db.get_cache_stats()['size']} (LRU eviction)"
)

# Verify id=2 is not in cache (cache miss)
stats_before = small_cache_db.get_cache_stats()['misses']
small_cache_db.find({"id": 2})
stats_after = small_cache_db.get_cache_stats()['misses']
result = 'Cache miss (evicted)' if stats_after > stats_before else 'Cache hit'
print(f"Query for id=2: {result}\n")

# Final stats
print("--- Final Cache Statistics ---")
final_stats = db.get_cache_stats()
print(f"Total hits: {final_stats['hits']}")
print(f"Total misses: {final_stats['misses']}")
print(f"Hit rate: {final_stats['hit_rate']}")

print("\n✓ Demo complete!")
print("\nTo learn more, check out CACHING.md")
