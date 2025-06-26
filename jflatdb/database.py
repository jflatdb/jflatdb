"""
Main JSONDatabase class
"""

from .storage import Storage
from .schema import Schema
from .security import Security
from .indexer import Indexer
from .query_engine import QueryEngine 
from .utils.logger import Logger

class Database:
    def __init__(self, path, password):
        self.logger = Logger()
        self.path = path
        self.storage = Storage(path)
        self.schema = Schema()
        self.security = Security(password)
        self.indexer = Indexer()
        self.data = self.load()
        self.query_engine = QueryEngine(self.data) 
        self.logger.info("Database initialized") # test logger

    def load(self):
        raw = self.storage.read()
        return self.security.decrypt(raw)

    def save(self):
        encrypted = self.security.encrypt(self.data)
        self.storage.write(encrypted)
        self.query_engine = QueryEngine(self.data)

    def insert(self, record: dict):
        self.schema.validate(record)
        self.data.append(record)
        self.logger.info(f"Inserted record: {record}") # Logger Test
        self.indexer.build(self.data)
        self.save()

    def find(self, query: dict):
        return self.indexer.query(self.data, query)

    def update(self, query, updates):
        found = self.find(query)
        for item in found:
            item.update(updates)
        self.save()

    def delete(self, query):
        self.data = [d for d in self.data if not all(d[k] == v for k, v in query.items())]
        self.save()
        
    # ----------- BUILT-IN QUERY FUNCTIONS ------------
    def min(self, column):
        return self.query_engine.min(column)

    def max(self, column):
        return self.query_engine.max(column)

    def avg(self, column):
        return self.query_engine.avg(column)

    def count(self, column=None):
        return self.query_engine.count(column)

    def between(self, column, low, high):
        return self.query_engine.between(column, low, high)

    def group_by(self, column):
        return self.query_engine.group_by(column)