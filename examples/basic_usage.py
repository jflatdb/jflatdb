"""
Basic usage demo for jflatdb
Run: python examples/basic_usage.py
"""

from jflatdb.database import Database


def main() -> None:
    # Create or connect to a database file (stored under data/ per Storage)
    db = Database("users.json", password="demo-password")

    # Optional: define a simple schema for validation
    db.schema.define(
        {
            "id": {"type": int, "required": True},
            "name": {"type": str, "required": True},
            "email": {"type": str, "required": False},
        }
    )

    # Clean slate for demo: delete any existing demo users by ids we use below
    for demo_id in [1, 2, 3]:
        db.delete({"id": demo_id})

    print("\n== Insert sample users ==")
    db.insert({"id": 1, "name": "Alice", "email": "alice@example.com"})
    db.insert({"id": 2, "name": "Bob", "email": "bob@example.com"})
    print("All users after insert:")
    print(db.find({}))  # empty query returns all per indexer.query

    print("\n== Find Bob ==")
    print(db.find({"name": "Bob"}))

    print("\n== Update Bob's email ==")
    db.update({"name": "Bob"}, {"email": "bob@updated.com"})
    print(db.find({"name": "Bob"}))

    print("\n== Delete Alice ==")
    db.delete({"name": "Alice"})

    print("\n== Final state ==")
    print(db.find({}))


if __name__ == "__main__":
    main()


