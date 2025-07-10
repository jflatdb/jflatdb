"""
Insert Records
-------------------------
Step by Step
1. Extra Information
    ✅ Adds new student entries into the students table.
    Data must match the column structure.
"""

from jflatdb.database import Database

db = Database("school.json", password="1234") # Creates or loads school.json

#db.insert({"id": 1, "name": "Alice"})
#db.insert({"id": 3, "name": "Lucky", "email": "lucky@example.com"})