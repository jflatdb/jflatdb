"""
Create Table with Constraints
-------------------------
Step by Step
1. Extra Information
    📝 Creates a table named students with specified column headers.
    If the table already exists, this will raise an error (or silently ignore if built-in logic handles duplicates).
"""

from jflatdb.database import Database

db = Database("school.json", password="1234") # Creates or loads school.json

# Learn this & modify for your requirement
db.schema.define({
    "id": {"type": int, "required": True},
    "name": {"type": str, "required": True},
    "email": {"type": str, "required": False, "default": "N/A"}
})