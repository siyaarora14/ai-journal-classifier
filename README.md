# Overview
I chose project option 1 which is a command-line interface journaling tool that classifies the emotion that best captures a journal entry the user inputs using zero-shot text classification. Users can:
- Add new journal entries “--add”
- Retrieve the last 3 entries “--last”
- Receive a classification tag; for example: Positive, Stressed, Excited, etc.

All entries are locally stored in a JSON file called journal_entries.json.

# Features

## 1. Zero-Shot Text Classification
The system uses the BART-large-MNLI model to classify sentiment and emotional tone without any model-specific training. Zero-shot classification is when a model can classify data into custom categories without ever seeing a labeled example or being trained on those specific categories.

## 2. Parser for data preprocessing and cleaning
When users input text there’s many factors to take into account like slang, emojis, abbreviations, and inconsistent spacing, because the BART model won’t give back an accurate classification if it takes in this raw text. The parser helps clean this data up so it can be fed into the model. Using argparse helps create well-defined flags (--add, --last) and makes sure that a user’s input is validated and organized properly. 

The parser:
- Translates modern Slang to more dictionary defined terminology 
- Maps emojis to text
- Lowercases all raw text 
- Performs regular expression cleaning 
- Normalizes whitespaces

This makes sure that the classifier model can take in cleaned up input which will increase the performance.

## 3. Local JSON Storage
Journal entries are stored in data/journal_entries.json with fields:
- timestamp
- raw_text
- cleaned_text
- classified_text (classification result)
- tag (classification result)

This format for the entries helps makes the data:
- Readable by humans so it’s user friendly 
- Easy to debug

## 4. Command-Line Interface
Users interact with the project through optional flags:
- `--add "your journal text here"` # inserts journal entry 
- `--last` # shows the last 3 journal entries or all journal entries if less than three

# Methodology

## 1. Model and Classification Logic
Tool: Hugging Face transformers library (facebook/bart-large-mnli via the pipeline API).

- I define get_zero_shot_classifier() in core/models.py, which returns a zero-shot classification pipeline initialized with the BART-large-MNLI model
- In core/classifier.py, I call this once and store it in a variable (zsPipeline) so the model is loaded only once and reused

classify_text(cleaned_text):
- If cleaned_text is empty or only whitespace, it immediately returns "Neutral" to avoid sending meaningless input to the model.
- Otherwise, it calls zsPipeline(cleaned_text, candidate_labels=labels, multi_label=False) and returns the top label from the model’s output.

### How I verified this:
- I tested positive, negative, and stressed entries to see if the tags were right
- In tests (tests/test_classifier.py), I mocked the pipeline with a FakePipeline and used monkeypatch to replace the real model. This lets me:
  - Confirm that classify_text() is right
  - Test behavior for normal input, and for edge cases like empty strings

## 2. Parsing and Text Normalization
Tools: Python string methods and the re module (regular expressions), plus custom slang and emoji mappings in core/parser.py which I prompted ChatGPT to create for me.

clean_text(raw_text):
- Lowercases all the raw text from the journal entries 
- Replaces emojis using a dictionary that maps common emojis to words that describe it 
- Translates slang to more dictionary defined language
- Uses regular expressions to remove unwanted symbols and normalize whitespace
- Returns a clean string

### How I verified this:
- I wrote unit tests in tests/test_parser.py that check: 
  - Slang translation
  - Emoji conversion
  - Regex-based cleanup where repeating punctuation and spacing are removed
- I also manually tested journal entries with combinations of slang, emojis, and punctuation

## 3. Storage Layer and Data Integrity
Tool: Python’s built-in json module and file I/O operations, implemented in storage/database.py

add_entry(raw_text, cleaned_text, tag, timestamp):
- Loads existing entries from data/journal_entries.json if the file exists
- Adds a new entry with all fields 
- Writes back to disk as a list of JSON objects

get_last_entries():
- Loads all entries
- Returns the last n entries in order

### How I verified this:
- In tests/test_database.py, I used tmp_path and monkeypatch to redirect file operations to a temporary test file so that tests don’t mess with real data
- The test calls add_entry() and then get_last_entries() and makes sure that:
  - The right number of entries returns
  - The tag field matches what was written

## 4. CLI Behavior and Input Validation
Tool: Python’s argparse library, with all CLI logic in main.py.

- argparse defines two optional arguments: --add (string) and --last
- When --add is entered: 
  - The raw input text is checked for being empty or whitespace only, and if it is, the program prints an error and returns
  - Otherwise, it goes through: clean_text -> classify_text -> add_entry

- When --last is entered by the user:
  - The program calls get_last_entries(n) and prints the last 3 entries (or all of them if less than 3) in a readable format

### How I verified this:
- I ran combinations of flags (only --add, only --last, both, and invalid input).
- I checked that:
  - Empty journal entries are rejected
  - Valid entries are classified and stored
  - Retrieval and display work right 

# Requirements & Installation

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run the CLI

python3 main.py --add "your text"
python3 main.py --last


# Testing
Unit tests are in the `tests/` directory.

Run all tests:

pytest -v

Tests cover:
- Parser correctness
- Classification
- Storage read/write logic

# Why My Solution Is Maintainable
- Code is modular and each function does one thing well
- Clear separation between parsing, classification, storage, and CLI
- Local JSON logs make debugging simple
- Tests ensure reliability

# Possible Future Improvements
- Add user defined labels to classify journals
- Add encryption for journal privacy
- Build a web UI
