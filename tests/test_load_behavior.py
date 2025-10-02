import os
import pytest

import jflatdb.storage as storage_module
from jflatdb.database import Database


def _patch_storage_init_to_tmp(tmp_path, monkeypatch):
    def _init(self, filename):
        self.folder = str(tmp_path)
        self.filepath = os.path.join(self.folder, filename)
        os.makedirs(self.folder, exist_ok=True)
        return None

    monkeypatch.setattr(storage_module.Storage, "__init__", _init)


def test_missing_file_initializes_empty(tmp_path, monkeypatch):
    # Ensure Storage writes/reads from tmp_path
    _patch_storage_init_to_tmp(tmp_path, monkeypatch)

    db = Database('missing.json', password='x')
    assert db.data == []


def test_empty_file_initializes_empty(tmp_path, monkeypatch):
    _patch_storage_init_to_tmp(tmp_path, monkeypatch)

    path = os.path.join(tmp_path, 'empty.json')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')

    db = Database('empty.json', password='x')
    assert db.data == []


def test_corrupt_file_raises_runtimeerror(tmp_path, monkeypatch):
    _patch_storage_init_to_tmp(tmp_path, monkeypatch)

    # Write text that will not eval to a list after decryption
    path = os.path.join(tmp_path, 'corrupt.json')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('not-encrypted-garbage')

    with pytest.raises(RuntimeError):
        Database('corrupt.json', password='x')
