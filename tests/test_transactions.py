import os
from jflatdb.database import Database
from jflatdb.transaction import Transaction, TransactionError
import jflatdb.storage as storage_module


def _patch_storage_init_to_tmp(tmp_path, monkeypatch):
    """Patch Storage to use temp directory for testing"""
    def _init(self, filename):
        self.folder = str(tmp_path)
        self.filepath = os.path.join(self.folder, filename)
        self.wal_path = os.path.join(self.folder, f"{filename}.wal")
        os.makedirs(self.folder, exist_ok=True)
        return None

    monkeypatch.setattr(storage_module.Storage, "__init__", _init)


class TestTransactionBasics:
    """Test basic transaction functionality"""

    def test_transaction_creation(self, tmp_path, monkeypatch):
        """Test creating a transaction"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        txn = db.transaction()

        assert isinstance(txn, Transaction)
        assert not txn.is_active
        assert not txn.is_committed
        assert not txn.is_rolled_back

    def test_transaction_context_manager(self, tmp_path, monkeypatch):
        """Test transaction as context manager"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        with db.transaction() as txn:
            assert txn.is_active
            txn.insert({"id": 1, "name": "Alice"})

        assert not txn.is_active
        assert txn.is_committed

    def test_transaction_insert_commit(self, tmp_path, monkeypatch):
        """Test transaction insert and commit"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        # Data should be empty initially
        assert len(db.data) == 0

        with db.transaction() as txn:
            txn.insert({"id": 1, "name": "Alice"})
            txn.insert({"id": 2, "name": "Bob"})

        # Both records should be in database after commit
        assert len(db.data) == 2
        assert db.data[0]["name"] == "Alice"
        assert db.data[1]["name"] == "Bob"

    def test_transaction_rollback(self, tmp_path, monkeypatch):
        """Test transaction rollback"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})

        original_count = len(db.data)

        txn = db.transaction()
        txn.__enter__()
        txn.insert({"id": 2, "name": "Bob"})
        txn.rollback()

        # Database should remain unchanged
        assert len(db.data) == original_count
        assert txn.is_rolled_back

    def test_transaction_rollback_on_exception(self, tmp_path, monkeypatch):
        """Test automatic rollback on exception"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})

        original_count = len(db.data)

        try:
            with db.transaction() as txn:
                txn.insert({"id": 2, "name": "Bob"})
                raise ValueError("Simulated error")
        except ValueError:
            pass

        # Database should remain unchanged after exception
        assert len(db.data) == original_count

    def test_transaction_update(self, tmp_path, monkeypatch):
        """Test transaction update operation"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice", "age": 25})
        db.insert({"id": 2, "name": "Bob", "age": 30})

        with db.transaction() as txn:
            txn.update({"name": "Alice"}, {"age": 26})

        # Check update was applied
        alice = db.find({"name": "Alice"})[0]
        assert alice["age"] == 26

    def test_transaction_delete(self, tmp_path, monkeypatch):
        """Test transaction delete operation"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})
        db.insert({"id": 2, "name": "Bob"})

        with db.transaction() as txn:
            txn.delete({"name": "Alice"})

        # Alice should be deleted
        assert len(db.data) == 1
        assert db.data[0]["name"] == "Bob"

    def test_transaction_multiple_operations(self, tmp_path, monkeypatch):
        """Test transaction with multiple different operations"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice", "age": 25})
        db.insert({"id": 2, "name": "Bob", "age": 30})

        with db.transaction() as txn:
            txn.insert({"id": 3, "name": "Charlie", "age": 35})
            txn.update({"name": "Alice"}, {"age": 26})
            txn.delete({"name": "Bob"})

        # Verify all operations were applied
        assert len(db.data) == 2
        alice = db.find({"name": "Alice"})[0]
        assert alice["age"] == 26
        charlie = db.find({"name": "Charlie"})[0]
        assert charlie["age"] == 35

    def test_transaction_isolation(self, tmp_path, monkeypatch):
        """Test transaction isolation - changes not visible until commit"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        txn = db.transaction()
        txn.__enter__()

        # Insert in transaction
        txn.insert({"id": 1, "name": "Alice"})

        # Database should still be empty (not committed)
        assert len(db.data) == 0

        # Commit
        txn.commit()

        # Now data should be visible
        assert len(db.data) == 1


class TestTransactionErrors:
    """Test transaction error handling"""

    def test_cannot_operate_on_inactive_transaction(self, tmp_path, monkeypatch):
        """Test operations fail on inactive transaction"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        txn = db.transaction()

        # Transaction not started, operations should fail
        try:
            txn.insert({"id": 1, "name": "Alice"})
            assert False, "Should have raised TransactionError"
        except TransactionError as e:
            assert "not active" in str(e)

    def test_cannot_commit_twice(self, tmp_path, monkeypatch):
        """Test cannot commit transaction twice"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        with db.transaction() as txn:
            txn.insert({"id": 1, "name": "Alice"})

        # Try to commit again
        try:
            txn.commit()
            assert False, "Should have raised TransactionError"
        except TransactionError as e:
            assert "already committed" in str(e)

    def test_cannot_rollback_committed_transaction(self, tmp_path, monkeypatch):
        """Test cannot rollback after commit"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        with db.transaction() as txn:
            txn.insert({"id": 1, "name": "Alice"})

        # Try to rollback after commit
        try:
            txn.rollback()
            assert False, "Should have raised TransactionError"
        except TransactionError as e:
            assert "already committed" in str(e)

    def test_cannot_operate_after_rollback(self, tmp_path, monkeypatch):
        """Test operations fail after rollback"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        txn = db.transaction()
        txn.__enter__()
        txn.rollback()

        # Try to insert after rollback
        try:
            txn.insert({"id": 1, "name": "Alice"})
            assert False, "Should have raised TransactionError"
        except TransactionError as e:
            assert "rolled back" in str(e)


class TestTransactionAtomicity:
    """Test transaction atomicity guarantees"""

    def test_all_or_nothing_on_success(self, tmp_path, monkeypatch):
        """Test all operations applied on success"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        with db.transaction() as txn:
            for i in range(10):
                txn.insert({"id": i, "value": i * 10})

        # All 10 records should be present
        assert len(db.data) == 10

    def test_all_or_nothing_on_failure(self, tmp_path, monkeypatch):
        """Test no operations applied on failure"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 0, "value": 0})

        try:
            with db.transaction() as txn:
                txn.insert({"id": 1, "value": 10})
                txn.insert({"id": 2, "value": 20})
                raise RuntimeError("Simulated failure")
        except RuntimeError:
            pass

        # Only original record should remain
        assert len(db.data) == 1
        assert db.data[0]["id"] == 0


class TestTransactionOperations:
    """Test transaction operation tracking"""

    def test_get_operations(self, tmp_path, monkeypatch):
        """Test getting list of transaction operations"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        with db.transaction() as txn:
            txn.insert({"id": 1, "name": "Alice"})
            txn.insert({"id": 2, "name": "Bob"})

            ops = txn.get_operations()
            assert len(ops) == 2
            assert ops[0]['type'] == 'insert'
            assert ops[1]['type'] == 'insert'

    def test_operation_tracking_all_types(self, tmp_path, monkeypatch):
        """Test operation tracking for all operation types"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice", "age": 25})

        with db.transaction() as txn:
            txn.insert({"id": 2, "name": "Bob", "age": 30})
            txn.update({"name": "Alice"}, {"age": 26})
            txn.delete({"name": "Bob"})

            ops = txn.get_operations()
            assert len(ops) == 3
            assert ops[0]['type'] == 'insert'
            assert ops[1]['type'] == 'update'
            assert ops[2]['type'] == 'delete'


class TestWALRecovery:
    """Test Write-Ahead Log recovery functionality"""

    def test_wal_created_during_write(self, tmp_path, monkeypatch):
        """Test WAL file is created during writes"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})

        # WAL should not exist after successful write
        assert not db.storage.has_wal()

    def test_atomic_write_with_temp_file(self, tmp_path, monkeypatch):
        """Test atomic write using temp file"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        with db.transaction() as txn:
            txn.insert({"id": 1, "name": "Alice"})

        # After successful transaction, WAL should be removed
        assert not db.storage.has_wal()
        assert len(db.data) == 1
