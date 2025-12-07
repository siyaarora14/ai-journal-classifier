from core.parser import clean_text
from core.classifier import classify_text
from storage.database import add_entry, get_last_entries
from datetime import datetime
import argparse 

def main():
    cli = argparse.ArgumentParser(
        description="Zero-Shot Text Classification Application"
    )
    cli.add_argument(
        "--add", metavar="TEXT", type=str, help="Add journal entry"
    )
    cli.add_argument(
        "--last", action="store_true",
        help="Return a formatted summary of the last 3 entries with their tags"
    )

    args = cli.parse_args()

    if args.add:
        raw_text = args.add
        if not raw_text or not raw_text.strip():
            print("Error: Cannot add empty journal entry")
            return
        
        try:
            cleaned_text = clean_text(raw_text)
            classified_text = classify_text(cleaned_text)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_entry(raw_text, cleaned_text, classified_text, timestamp)
            print("journal entry added !!")
        except Exception as e:
            print(f"Error processing journal entry: {e}")
            return

    if args.last:
        # Return formatted summary of last 3 entries (per requirement)
        entries = get_last_entries(3)
        
        if not entries:
            print("No journal entries found.")
            return

        print(f"\n=== Last 3 Journal Entries ===\n")
        for i, entry in enumerate(entries, 1):
            tag = entry.get('tag') or entry.get('classified_text', 'Unknown')
            print(f"{i}. [{entry['timestamp']}]")
            print(f"   Entry: {entry['raw_text']}")
            print(f"   Emotion: {tag}\n")
        
        print("=" * 40)


if __name__ == "__main__":
    main()


