import os
from jflatdb.database import Database
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


class TestDatabaseMigration:
    """Test database migration integration"""

    def test_migrate_schema_add_field(self, tmp_path, monkeypatch):
        """Test migrating schema by adding a field"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})
        db.insert({"id": 2, "name": "Bob"})

        # Verify initial schema version
        assert db.get_schema_version() == 0

        # Migrate: add status field
        def add_status(migration):
            migration.add_field("status", "active")

        db.migrate_schema(add_status, "Add status field")

        # Verify migration applied
        assert db.data[0]["status"] == "active"
        assert db.data[1]["status"] == "active"

        # Verify version incremented
        assert db.get_schema_version() == 1

    def test_migrate_schema_rename_field(self, tmp_path, monkeypatch):
        """Test migrating schema by renaming a field"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "fullname": "Alice Smith"})
        db.insert({"id": 2, "fullname": "Bob Jones"})

        def rename_fullname(migration):
            migration.rename_field("fullname", "name")

        db.migrate_schema(rename_fullname, "Rename fullname to name")

        assert "fullname" not in db.data[0]
        assert db.data[0]["name"] == "Alice Smith"
        assert db.get_schema_version() == 1

    def test_migrate_schema_remove_field(self, tmp_path, monkeypatch):
        """Test migrating schema by removing a field"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice", "temp": "remove_me"})
        db.insert({"id": 2, "name": "Bob", "temp": "remove_me"})

        def remove_temp(migration):
            migration.remove_field("temp")

        db.migrate_schema(remove_temp, "Remove temp field")

        assert "temp" not in db.data[0]
        assert "temp" not in db.data[1]
        assert db.get_schema_version() == 1

    def test_migrate_schema_set_default(self, tmp_path, monkeypatch):
        """Test migrating schema by setting defaults"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})
        db.insert({"id": 2, "name": "Bob", "email": "bob@example.com"})

        def set_email_default(migration):
            migration.set_default("email", "unknown@example.com")

        db.migrate_schema(set_email_default, "Set default email")

        assert db.data[0]["email"] == "unknown@example.com"
        assert db.data[1]["email"] == "bob@example.com"

    def test_migrate_schema_multiple_operations(self, tmp_path, monkeypatch):
        """Test migration with multiple operations"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "fullname": "Alice"})
        db.insert({"id": 2, "fullname": "Bob"})

        def complex_migration(migration):
            migration.rename_field("fullname", "name")
            migration.add_field("status", "active")
            migration.add_field("created_at", "NOW()")

        db.migrate_schema(complex_migration, "Complex schema update")

        assert "fullname" not in db.data[0]
        assert db.data[0]["name"] == "Alice"
        assert db.data[0]["status"] == "active"
        assert "created_at" in db.data[0]

    def test_migration_history_tracking(self, tmp_path, monkeypatch):
        """Test migration history is tracked correctly"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        def migration1(m):
            m.add_field("field1", "value1")

        def migration2(m):
            m.add_field("field2", "value2")

        db.migrate_schema(migration1, "First migration")
        db.migrate_schema(migration2, "Second migration")

        history = db.get_migration_history()
        assert len(history) == 2
        assert history[0]["name"] == "First migration"
        assert history[1]["name"] == "Second migration"
        assert history[0]["from_version"] == 0
        assert history[0]["to_version"] == 1
        assert history[1]["from_version"] == 1
        assert history[1]["to_version"] == 2

    def test_migration_persists_to_disk(self, tmp_path, monkeypatch):
        """Test migration persists to disk and reloads correctly"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        # Create database and perform migration
        db1 = Database('test.json', password='test')
        db1.insert({"id": 1, "name": "Alice"})

        def add_status(m):
            m.add_field("status", "active")

        db1.migrate_schema(add_status, "Add status field")

        # Reload database in new instance
        db2 = Database('test.json', password='test')

        # Verify migrated data persisted
        assert len(db2.data) == 1
        assert db2.data[0]["status"] == "active"

        # Verify schema version persisted
        assert db2.get_schema_version() == 1

    def test_migration_invalidates_cache(self, tmp_path, monkeypatch):
        """Test migration invalidates query cache"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test', cache_enabled=True)
        db.insert({"id": 1, "name": "Alice"})

        # Populate cache
        result1 = db.find({"name": "Alice"})
        assert len(result1) == 1

        # Perform migration
        def add_status(m):
            m.add_field("status", "active")

        db.migrate_schema(add_status, "Add status")

        # Query should return updated data (not cached)
        result2 = db.find({"name": "Alice"})
        assert result2[0]["status"] == "active"

    def test_migration_with_special_keywords(self, tmp_path, monkeypatch):
        """Test migration with special default value keywords"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1})
        db.insert({"id": 2})

        def add_timestamps_and_ids(m):
            m.add_field("created_at", "NOW()")
            m.add_field("unique_id", "UUID()")
            m.add_field("count", "ZERO()")

        db.migrate_schema(add_timestamps_and_ids, "Add metadata fields")

        # Verify special keywords resolved
        assert "created_at" in db.data[0]
        assert isinstance(db.data[0]["created_at"], str)
        assert db.data[0]["unique_id"] != db.data[1]["unique_id"]
        assert db.data[0]["count"] == 0

    def test_empty_database_migration(self, tmp_path, monkeypatch):
        """Test migration on empty database"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')

        def add_field(m):
            m.add_field("status", "active")

        db.migrate_schema(add_field, "Add status to empty db")

        # Should complete without error
        assert db.get_schema_version() == 1
        assert len(db.data) == 0

    def test_sequential_migrations(self, tmp_path, monkeypatch):
        """Test multiple sequential migrations"""
        _patch_storage_init_to_tmp(tmp_path, monkeypatch)

        db = Database('test.json', password='test')
        db.insert({"id": 1, "name": "Alice"})

        # Migration 1: Add email
        db.migrate_schema(
            lambda m: m.add_field("email", "unknown@example.com"),
            "Add email"
        )

        # Migration 2: Add status
        db.migrate_schema(
            lambda m: m.add_field("status", "active"),
            "Add status"
        )

        # Migration 3: Rename name to fullname
        db.migrate_schema(
            lambda m: m.rename_field("name", "fullname"),
            "Rename name"
        )

        # Verify all migrations applied
        assert "name" not in db.data[0]
        assert db.data[0]["fullname"] == "Alice"
        assert db.data[0]["email"] == "unknown@example.com"
        assert db.data[0]["status"] == "active"
        assert db.get_schema_version() == 3
