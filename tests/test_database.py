import os
import json
from storage.database import add_entry, get_last_entries, FILE_PATH

def test_storage_write_and_read(tmp_path, monkeypatch):
    test_file = tmp_path / "test.json"
    
    monkeypatch.setattr("storage.database.FILE_PATH", str(test_file))
    
    add_entry("raw", "clean", "Positive", "2025-12-06 00:00:00")
    entries = get_last_entries(1)
    
    assert len(entries) == 1
    assert entries[0]["tag"] == "Positive"
