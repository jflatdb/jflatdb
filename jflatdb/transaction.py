"""
Transaction support for atomic database operations
"""

import copy
from typing import Dict, List, Any
from .utils.logger import Logger


class TransactionError(Exception):
    """Raised when a transaction operation fails"""
    pass


class Transaction:
    """
    Provides ACID transaction support for database operations.

    Supports:
    - Atomicity: All operations succeed or none are applied
    - Consistency: Database remains in valid state
    - Isolation: Changes invisible until commit
    - Context manager: with db.transaction() as txn:
    """

    def __init__(self, database):
        """
        Initialize a new transaction.

        Args:
            database: The Database instance this transaction belongs to
        """
        self.db = database
        self.logger = Logger()
        self._active = False
        self._committed = False
        self._rolled_back = False

        # Create a deep copy of data to work with
        self._data_snapshot = copy.deepcopy(database.data)
        self._operations: List[Dict[str, Any]] = []

    def __enter__(self):
        """Enter transaction context"""
        self._active = True
        self.logger.info("Transaction started")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit transaction context.

        Auto-commits if no exception occurred, otherwise rolls back.
        """
        if exc_type is not None:
            # Exception occurred, rollback
            self.rollback()
            return False  # Re-raise the exception

        if self._active and not self._committed and not self._rolled_back:
            # No exception, commit the transaction
            self.commit()

        return True

    def insert(self, record: Dict[str, Any]):
        """
        Queue an insert operation.

        Args:
            record: Dictionary record to insert

        Raises:
            TransactionError: If transaction is not active
        """
        if self._committed:
            raise TransactionError("Cannot insert: transaction already committed")

        if self._rolled_back:
            raise TransactionError("Cannot insert: transaction rolled back")

        if not self._active:
            raise TransactionError("Cannot insert: transaction not active")

        # Validate using database schema
        self.db.schema.validate(record, self._data_snapshot)

        # Add to working copy
        self._data_snapshot.append(record)

        # Track operation for logging
        self._operations.append({
            'type': 'insert',
            'record': record
        })

        self.logger.info(f"Transaction: queued insert {record}")

    def update(self, query: Dict[str, Any], updates: Dict[str, Any]):
        """
        Queue an update operation.

        Args:
            query: Query to find records to update
            updates: Fields to update

        Raises:
            TransactionError: If transaction is not active
        """
        if not self._active:
            raise TransactionError("Cannot update: transaction not active")

        if self._committed:
            raise TransactionError("Cannot update: transaction already committed")

        if self._rolled_back:
            raise TransactionError("Cannot update: transaction rolled back")

        # Find matching records in working copy using simple matching
        found = [
            item for item in self._data_snapshot
            if all(item.get(k) == v for k, v in query.items())
        ]

        if not found:
            self.logger.warn(f"Transaction: no records found for update query {query}")

        # Apply updates to working copy
        for item in found:
            item.update(updates)

        # Track operation
        self._operations.append({
            'type': 'update',
            'query': query,
            'updates': updates,
            'affected': len(found)
        })

        self.logger.info(f"Transaction: queued update for {len(found)} records")

    def delete(self, query: Dict[str, Any]):
        """
        Queue a delete operation.

        Args:
            query: Query to find records to delete

        Raises:
            TransactionError: If transaction is not active
        """
        if not self._active:
            raise TransactionError("Cannot delete: transaction not active")

        if self._committed:
            raise TransactionError("Cannot delete: transaction already committed")

        if self._rolled_back:
            raise TransactionError("Cannot delete: transaction rolled back")

        # Count records before deletion
        before_count = len(self._data_snapshot)

        # Delete from working copy
        self._data_snapshot = [
            d for d in self._data_snapshot
            if not all(d.get(k) == v for k, v in query.items())
        ]

        affected = before_count - len(self._data_snapshot)

        # Track operation
        self._operations.append({
            'type': 'delete',
            'query': query,
            'affected': affected
        })

        self.logger.info(f"Transaction: queued delete for {affected} records")

    def commit(self):
        """
        Commit the transaction, applying all changes atomically.

        Raises:
            TransactionError: If transaction cannot be committed
        """
        if self._committed:
            raise TransactionError("Transaction already committed")

        if self._rolled_back:
            raise TransactionError("Cannot commit: transaction was rolled back")

        if not self._active:
            raise TransactionError("Cannot commit: transaction not active")

        try:
            # Apply changes atomically
            self.db.data = self._data_snapshot
            self.db.indexer.build(self.db.data)
            self.db.cache.invalidate()
            self.db.save()

            self._committed = True
            self._active = False

            self.logger.info(
                f"Transaction committed successfully: {len(self._operations)} operations"
            )

        except Exception as e:
            self.logger.error(f"Transaction commit failed: {e}")
            raise TransactionError(f"Failed to commit transaction: {e}") from e

    def rollback(self):
        """
        Rollback the transaction, discarding all changes.
        """
        if self._committed:
            raise TransactionError("Cannot rollback: transaction already committed")

        if self._rolled_back:
            self.logger.warn("Transaction already rolled back")
            return

        # Discard working copy
        self._data_snapshot = []
        self._operations = []
        self._rolled_back = True
        self._active = False

        self.logger.info("Transaction rolled back")

    def get_operations(self) -> List[Dict[str, Any]]:
        """
        Get list of operations queued in this transaction.

        Returns:
            List of operation dictionaries
        """
        return self._operations.copy()

    @property
    def is_active(self) -> bool:
        """Check if transaction is currently active"""
        return self._active

    @property
    def is_committed(self) -> bool:
        """Check if transaction has been committed"""
        return self._committed

    @property
    def is_rolled_back(self) -> bool:
        """Check if transaction has been rolled back"""
        return self._rolled_back
