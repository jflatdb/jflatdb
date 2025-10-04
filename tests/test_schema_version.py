import os
from jflatdb.schema_version import SchemaVersion


class TestSchemaVersion:
    """Test suite for SchemaVersion class"""

    def test_initialization_creates_metadata(self, tmp_path):
        """Test that SchemaVersion initializes with default metadata"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        assert sv.get_version() == 0
        assert os.path.exists(sv.metadata_file)

        metadata = sv.get_metadata()
        assert 'version' in metadata
        assert 'created_at' in metadata
        assert 'updated_at' in metadata
        assert 'migrations' in metadata
        assert metadata['migrations'] == []

    def test_increment_version(self, tmp_path):
        """Test version increment"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        assert sv.get_version() == 0

        sv.increment_version('First migration')
        assert sv.get_version() == 1

        sv.increment_version('Second migration')
        assert sv.get_version() == 2

    def test_migration_history(self, tmp_path):
        """Test migration history tracking"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        sv.increment_version('Add created_at field')
        sv.increment_version('Rename fullname to name')

        history = sv.get_migration_history()
        assert len(history) == 2

        assert history[0]['from_version'] == 0
        assert history[0]['to_version'] == 1
        assert history[0]['name'] == 'Add created_at field'
        assert 'timestamp' in history[0]

        assert history[1]['from_version'] == 1
        assert history[1]['to_version'] == 2
        assert history[1]['name'] == 'Rename fullname to name'

    def test_metadata_persistence(self, tmp_path):
        """Test that metadata persists across instances"""
        storage_folder = str(tmp_path)

        # Create and update version
        sv1 = SchemaVersion(storage_folder=storage_folder, db_name='test_version')
        sv1.increment_version('Initial migration')
        sv1.increment_version('Second migration')

        assert sv1.get_version() == 2

        # Create new instance and verify it loads existing metadata
        sv2 = SchemaVersion(storage_folder=storage_folder, db_name='test_version')
        assert sv2.get_version() == 2

        history = sv2.get_migration_history()
        assert len(history) == 2

    def test_reset(self, tmp_path):
        """Test schema version reset"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        sv.increment_version('Migration 1')
        sv.increment_version('Migration 2')
        sv.increment_version('Migration 3')

        assert sv.get_version() == 3
        assert len(sv.get_migration_history()) == 3

        sv.reset()

        assert sv.get_version() == 0
        assert sv.get_migration_history() == []

    def test_get_metadata_returns_copy(self, tmp_path):
        """Test that get_metadata returns a copy, not reference"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        metadata1 = sv.get_metadata()
        metadata1['version'] = 999  # Modify the copy

        # Original should be unchanged
        assert sv.get_version() == 0

    def test_multiple_increments_sequential(self, tmp_path):
        """Test multiple sequential version increments"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        for i in range(10):
            sv.increment_version(f'Migration {i+1}')

        assert sv.get_version() == 10
        assert len(sv.get_migration_history()) == 10

        # Verify sequential versioning
        history = sv.get_migration_history()
        for i, record in enumerate(history):
            assert record['from_version'] == i
            assert record['to_version'] == i + 1

    def test_empty_migration_name(self, tmp_path):
        """Test increment with empty migration name"""
        sv = SchemaVersion(storage_folder=str(tmp_path), db_name='test_version')

        sv.increment_version()  # No name provided
        assert sv.get_version() == 1

        history = sv.get_migration_history()
        assert history[0]['name'] == ''
