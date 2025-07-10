"""
# Usage Example / CLI Interface
"""

from jflatdb.database import Database

db = Database("db.json",password="1234")

db.schema.define({
    "id": {"type": int, "required": True},
    "name": {"type": str, "required": True},
    "email": {"type": str, "required": False, "default": "N/A"}
})

db.insert({"id": 1, "name": "Alice"})

#db.insert({"id": 3, "name": "Lucky", "email": "lucky@example.com"})

print(db.find({"id": 1}))
