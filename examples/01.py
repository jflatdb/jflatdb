"""
Create or open a database
-------------------------
Step by Step
1. Import Module
    `from jflatdb.database import Database`
2. Initialize the Database
    `db = Database("school.json", password="1234")`,
    `db = Database("create_database_name.json", password="make password")`
3. Extra Information
"""

from jflatdb.database import Database

db = Database("school.json", password="1234") # Creates or loads school.json
