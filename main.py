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
        "--last", metavar="NUMBER", type=int, help="Get last n journal entries"
    )

    args = cli.parse_args()

    if args.add:
        raw_text = args.add
        cleaned_text = clean_text(raw_text)
        classified_text = classify_text(cleaned_text)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_entry(raw_text, cleaned_text, classified_text, timestamp)
        print("journal entry added !!")

    if args.last:
        n = args.last
        entries = get_last_entries(n)
        for entry in entries:
            print(f"[{entry['timestamp']}] {entry['raw_text']} => {entry['classified_text']}") 
        


