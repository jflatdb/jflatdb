"""
Schema Migration Example for jflatdb

This example demonstrates how to use the schema migration feature to evolve
your database schema over time while preserving data integrity.
"""

from jflatdb.database import Database
import os

# Clean up any existing example data
if os.path.exists('data/migration_demo.json'):
    os.remove('data/migration_demo.json')
if os.path.exists('data/migration_demo_schema.json'):
    os.remove('data/migration_demo_schema.json')

print("=== jflatdb Schema Migration Demo ===\n")

# Initialize database
db = Database('migration_demo.json', password='demo123')
print("✓ Database initialized")
print(f"  Current schema version: {db.get_schema_version()}\n")

# Insert initial data with simple schema
print("Step 1: Insert initial user data")
db.insert({"id": 1, "username": "alice"})
db.insert({"id": 2, "username": "bob"})
db.insert({"id": 3, "username": "charlie"})
print("  Inserted 3 users")
print(f"  Sample record: {db.data[0]}\n")

# Migration 1: Add email field with default
print("Migration 1: Add email field with default value")


def add_email_field(migration):
    migration.add_field("email", "unknown@example.com")


db.migrate_schema(add_email_field, "Add email field")
print("✓ Migration complete")
print(f"  Schema version: {db.get_schema_version()}")
print(f"  Sample record: {db.data[0]}\n")

# Migration 2: Add timestamps
print("Migration 2: Add created_at timestamps")


def add_timestamps(migration):
    migration.add_field("created_at", "NOW()")


db.migrate_schema(add_timestamps, "Add timestamps")
print("✓ Migration complete")
print(f"  Schema version: {db.get_schema_version()}")
print(f"  Sample record: {db.data[0]}\n")

# Migration 3: Rename field
print("Migration 3: Rename username to name")


def rename_username(migration):
    migration.rename_field("username", "name")


db.migrate_schema(rename_username, "Rename username to name")
print("✓ Migration complete")
print(f"  Schema version: {db.get_schema_version()}")
print(f"  Sample record: {db.data[0]}\n")

# Migration 4: Add status with default
print("Migration 4: Add status field")


def add_status(migration):
    migration.add_field("status", "active")


db.migrate_schema(add_status, "Add user status")
print("✓ Migration complete")
print(f"  Schema version: {db.get_schema_version()}")
print(f"  Sample record: {db.data[0]}\n")

# Migration 5: Add unique IDs
print("Migration 5: Add unique IDs to each user")


def add_unique_ids(migration):
    migration.add_field("uuid", "UUID()")


db.migrate_schema(add_unique_ids, "Add UUID to users")
print("✓ Migration complete")
print(f"  Schema version: {db.get_schema_version()}")
print(f"  Sample record: {db.data[0]}")
print("  Note: Each user has a unique UUID\n")

# Display migration history
print("=== Migration History ===")
history = db.get_migration_history()
for i, migration in enumerate(history, 1):
    print(f"{i}. {migration['name']}")
    print(f"   Version {migration['from_version']} → {migration['to_version']}")
    print(f"   Timestamp: {migration['timestamp']}")

print(f"\n✓ Final schema version: {db.get_schema_version()}")
print(f"✓ Total migrations: {len(history)}")

# Demonstrate rollback on error
print("\n=== Rollback Demo ===")
print("Attempting migration that will fail...")


def failing_migration(migration):
    migration.add_field("temp", "value")
    raise RuntimeError("Intentional error to demonstrate rollback")


try:
    db.migrate_schema(failing_migration, "This will fail")
except RuntimeError:
    print("✓ Migration failed as expected")
    print(f"✓ Schema version unchanged: {db.get_schema_version()}")
    print("✓ Data rolled back successfully")
    print(f"  Sample record (no 'temp' field): {db.data[0]}")

print("\n=== Demo Complete ===")
print(f"Final schema version: {db.get_schema_version()}")
print(f"Total records: {len(db.data)}")
print("\nData files created:")
print("  - data/migration_demo.json (database)")
print("  - data/migration_demo_schema.json (version metadata)")
