"""
Exceptions Errors
"""

class DatabaseError(Exception):
    """Base class for all database errors"""
    pass

class SchemaError(DatabaseError):
    """Raised when data does not match schema"""
    pass

class QueryError(DatabaseError):
    """Raised for invalid query operations"""
    pass

class StorageError(DatabaseError):
    """Raised for file read/write problems"""
    pass

class SecurityError(DatabaseError):
    """Raised for encryption/decryption errors"""
    pass

class IndexingError(DatabaseError):
    """Raised for indexing-related issues"""
    pass
