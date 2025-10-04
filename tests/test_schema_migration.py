import pytest
from jflatdb.schema_migration import SchemaMigration, MigrationError


class TestAddField:
    """Test add_field migration operation"""

    def test_add_field_to_empty_dataset(self):
        """Test adding field to empty dataset"""
        data = []
        migration = SchemaMigration(data)
        migration.add_field("new_field", "default_value")

        assert len(data) == 0

    def test_add_field_with_simple_default(self):
        """Test adding field with simple default value"""
        data = [{"id": 1}, {"id": 2}, {"id": 3}]
        migration = SchemaMigration(data)
        migration.add_field("status", "active")

        for record in data:
            assert record["status"] == "active"

    def test_add_field_with_none_default(self):
        """Test adding field with None default"""
        data = [{"id": 1}, {"id": 2}]
        migration = SchemaMigration(data)
        migration.add_field("email", None)

        for record in data:
            assert "email" in record
            assert record["email"] is None

    def test_add_field_with_now_keyword(self):
        """Test adding field with NOW() special keyword"""
        data = [{"id": 1}]
        migration = SchemaMigration(data)
        migration.add_field("created_at", "NOW()")

        assert "created_at" in data[0]
        assert isinstance(data[0]["created_at"], str)
        assert "T" in data[0]["created_at"]  # ISO format check

    def test_add_field_with_uuid_keyword(self):
        """Test adding field with UUID() special keyword"""
        data = [{"id": 1}, {"id": 2}]
        migration = SchemaMigration(data)
        migration.add_field("unique_id", "UUID()")

        assert "unique_id" in data[0]
        assert "unique_id" in data[1]
        # UUIDs should be unique
        assert data[0]["unique_id"] != data[1]["unique_id"]
        # Should be UUID format (with dashes)
        assert "-" in data[0]["unique_id"]

    def test_add_field_skips_existing(self):
        """Test that add_field skips records that already have the field"""
        data = [
            {"id": 1, "status": "active"},
            {"id": 2},
            {"id": 3}
        ]
        migration = SchemaMigration(data)
        migration.add_field("status", "pending")

        assert data[0]["status"] == "active"  # Unchanged
        assert data[1]["status"] == "pending"  # Added
        assert data[2]["status"] == "pending"  # Added

    def test_add_field_empty_name_raises_error(self):
        """Test that empty field name raises error"""
        data = [{"id": 1}]
        migration = SchemaMigration(data)

        with pytest.raises(MigrationError, match="Field name cannot be empty"):
            migration.add_field("", "value")

    def test_add_field_special_keywords(self):
        """Test all special default keywords"""
        data = [{"id": 1}]
        migration = SchemaMigration(data)

        migration.add_field("zero", "ZERO()")
        migration.add_field("false", "FALSE()")
        migration.add_field("empty_str", "EMPTY_STRING()")
        migration.add_field("empty_list", "EMPTY_LIST()")
        migration.add_field("empty_dict", "EMPTY_DICT()")

        assert data[0]["zero"] == 0
        assert data[0]["false"] is False
        assert data[0]["empty_str"] == ""
        assert data[0]["empty_list"] == []
        assert data[0]["empty_dict"] == {}


class TestRemoveField:
    """Test remove_field migration operation"""

    def test_remove_field_from_all_records(self):
        """Test removing field from all records"""
        data = [
            {"id": 1, "temp": "x"},
            {"id": 2, "temp": "y"},
            {"id": 3, "temp": "z"}
        ]
        migration = SchemaMigration(data)
        migration.remove_field("temp")

        for record in data:
            assert "temp" not in record
            assert "id" in record

    def test_remove_field_partial_presence(self):
        """Test removing field when only some records have it"""
        data = [
            {"id": 1, "temp": "x"},
            {"id": 2},
            {"id": 3, "temp": "z"}
        ]
        migration = SchemaMigration(data)
        migration.remove_field("temp")

        for record in data:
            assert "temp" not in record

    def test_remove_nonexistent_field(self):
        """Test removing field that doesn't exist"""
        data = [{"id": 1}, {"id": 2}]
        migration = SchemaMigration(data)
        migration.remove_field("nonexistent")

        # Should complete without error
        assert len(data) == 2

    def test_remove_field_empty_name_raises_error(self):
        """Test that empty field name raises error"""
        data = [{"id": 1}]
        migration = SchemaMigration(data)

        with pytest.raises(MigrationError, match="Field name cannot be empty"):
            migration.remove_field("")


class TestRenameField:
    """Test rename_field migration operation"""

    def test_rename_field_all_records(self):
        """Test renaming field in all records"""
        data = [
            {"id": 1, "fullname": "Alice"},
            {"id": 2, "fullname": "Bob"},
            {"id": 3, "fullname": "Charlie"}
        ]
        migration = SchemaMigration(data)
        migration.rename_field("fullname", "name")

        for record in data:
            assert "fullname" not in record
            assert "name" in record

        assert data[0]["name"] == "Alice"
        assert data[1]["name"] == "Bob"
        assert data[2]["name"] == "Charlie"

    def test_rename_field_partial_presence(self):
        """Test renaming field when only some records have it"""
        data = [
            {"id": 1, "fullname": "Alice"},
            {"id": 2},
            {"id": 3, "fullname": "Charlie"}
        ]
        migration = SchemaMigration(data)
        migration.rename_field("fullname", "name")

        assert "name" in data[0]
        assert "name" not in data[1]  # Wasn't there originally
        assert "name" in data[2]
        assert "fullname" not in data[0]
        assert "fullname" not in data[2]

    def test_rename_field_conflict_raises_error(self):
        """Test that renaming to existing field raises error"""
        data = [
            {"id": 1, "fullname": "Alice", "name": "Al"}
        ]
        migration = SchemaMigration(data)

        with pytest.raises(MigrationError, match="already exists"):
            migration.rename_field("fullname", "name")

    def test_rename_field_empty_names_raise_error(self):
        """Test that empty field names raise error"""
        data = [{"id": 1, "field": "value"}]
        migration = SchemaMigration(data)

        with pytest.raises(MigrationError, match="Field names cannot be empty"):
            migration.rename_field("", "new_name")

        with pytest.raises(MigrationError, match="Field names cannot be empty"):
            migration.rename_field("field", "")

    def test_rename_field_same_name_raises_error(self):
        """Test that renaming to same name raises error"""
        data = [{"id": 1, "field": "value"}]
        migration = SchemaMigration(data)

        with pytest.raises(MigrationError, match="must be different"):
            migration.rename_field("field", "field")


class TestSetDefault:
    """Test set_default migration operation"""

    def test_set_default_for_missing_field(self):
        """Test setting default for missing fields"""
        data = [
            {"id": 1},
            {"id": 2, "status": "active"},
            {"id": 3}
        ]
        migration = SchemaMigration(data)
        migration.set_default("status", "pending")

        assert data[0]["status"] == "pending"
        assert data[1]["status"] == "active"  # Unchanged
        assert data[2]["status"] == "pending"

    def test_set_default_for_none_values(self):
        """Test setting default for None values"""
        data = [
            {"id": 1, "email": None},
            {"id": 2, "email": "alice@example.com"},
            {"id": 3, "email": None}
        ]
        migration = SchemaMigration(data)
        migration.set_default("email", "unknown@example.com")

        assert data[0]["email"] == "unknown@example.com"
        assert data[1]["email"] == "alice@example.com"  # Unchanged
        assert data[2]["email"] == "unknown@example.com"

    def test_set_default_with_special_keywords(self):
        """Test set_default with special keywords"""
        data = [{"id": 1}, {"id": 2}]
        migration = SchemaMigration(data)
        migration.set_default("created_at", "NOW()")

        assert "created_at" in data[0]
        assert "created_at" in data[1]

    def test_set_default_empty_name_raises_error(self):
        """Test that empty field name raises error"""
        data = [{"id": 1}]
        migration = SchemaMigration(data)

        with pytest.raises(MigrationError, match="Field name cannot be empty"):
            migration.set_default("", "value")


class TestGetData:
    """Test get_data method"""

    def test_get_data_returns_migrated_data(self):
        """Test that get_data returns the migrated dataset"""
        data = [{"id": 1}, {"id": 2}]
        migration = SchemaMigration(data)
        migration.add_field("status", "active")

        result = migration.get_data()
        assert result is data  # Same reference
        assert len(result) == 2
        assert result[0]["status"] == "active"


class TestMultipleOperations:
    """Test combining multiple migration operations"""

    def test_sequential_operations(self):
        """Test applying multiple migrations sequentially"""
        data = [
            {"id": 1, "fullname": "Alice"},
            {"id": 2, "fullname": "Bob"}
        ]
        migration = SchemaMigration(data)

        migration.rename_field("fullname", "name")
        migration.add_field("status", "active")
        migration.add_field("created_at", "NOW()")
        migration.set_default("email", "unknown@example.com")

        for record in data:
            assert "fullname" not in record
            assert "name" in record
            assert record["status"] == "active"
            assert "created_at" in record
            assert record["email"] == "unknown@example.com"
