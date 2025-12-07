import json
import os

# path to JSON file that's going to store all journal entries
FILE_PATH = "storage/journal_entries.json"


def _load_entries():
    """Load entries from the JSON file, and if it doesn't exist, return an empty list."""
    if not os.path.exists(FILE_PATH):
        return []  # no file yet so start with empty list

    with open(FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # if file is corrupted or empty, reset to empty list
            return []


def _save_entries(entries):
    """Save the list of entries back to the JSON file."""
    with open(FILE_PATH, "w") as file:
        json.dump(entries, file, indent=4)


def add_entry(raw_text, cleaned_text, tag, timestamp):
    """
    Add a new journal entry to the JSON file.
    Each entry stores raw text, cleaned text, tag, and timestamp.
    """
    entries = _load_entries()

    entry = {
        "timestamp": timestamp,
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "tag": tag,
        "classified_text": tag
    }

    entries.append(entry)
    _save_entries(entries)


def get_last_entries(n):
    """
    Return the last n journal entries.
    If there are fewer than n, return all entries.
    """
    entries = _load_entries()
    return entries[-n:] if n <= len(entries) else entries
