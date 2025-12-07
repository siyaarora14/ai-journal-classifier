import re

# slang dictionary just for data preprocessing
SLANG_MAP = {
    "idk": "i don't know",
    "idek": "i don't even know",
    "idc": "i don't care",
    "fr": "for real",
    "tbh": "to be honest",
    "fml": "my life feels hopeless",
    "lmao": "laughing",
    "lmfao": "laughing a lot",
    "lol": "laughing",
    "omg": "oh my god",
    "wtf": "what the hell",
    "smh": "shaking my head",
    "ngl": "not going to lie",
    "rn": "right now",
    "lowkey": "kind of",
    "highkey": "really",
    "mid": "disappointing",
    "af": "very",
    "bc": "because",
    "dunno": "do not know",
    "lmk": "let me know"
}


# emoji to text normalization
EMOJI_MAP = {
    "😢": "sad",
    "😭": "very sad",
    "😔": "upset",
    "😞": "disappointed",
    "😕": "confused",
    "😣": "frustrated",
    "😖": "anxious",
    "😫": "exhausted",
    "😩": "overwhelmed",
    "😡": "angry",
    "😠": "angry",
    "🤬": "furious",
    "😤": "annoyed",
    "🤯": "mind blown overwhelmed",
    "😳": "embarrassed",
    "🥺": "sad",
    "😃": "happy",
    "😀": "happy",
    "😊": "happy",
    "🙂": "content",
    "😍": "love",
    "🥰": "love",
    "❤️": "love",
    "💔": "heartbroken",
    "✨": "excited",
    "🔥": "excited",
    "👍": "good",
    "🙏": "grateful",
    "😴": "tired",
    "🥱": "tired",
    "🤢": "disgusted",
    "🤒": "sick",
    "🤕": "hurt",
    "🤡": "feeling foolish",
    "💀": "dead inside",
    "😐": "neutral", 
    "🤩": "excited",
    "😎": "cool", 
    "🙄": "annoyed"
}


def clean_text(raw_text):
    # convert to lowercase
    text = raw_text.lower()

    # replace emojis
    for emoji, meaning in EMOJI_MAP.items():
        text = text.replace(emoji, f" {meaning} ")

    # expand slang
    for slang, expansion in SLANG_MAP.items():
        text = text.replace(slang, expansion)

    # remove all characters except letters, numbers, and spaces
    text = re.sub(r"[^a-zA-Z0-9\s']", " ", text)

    # collapse multiple spaces into one
    text = re.sub(r"\s+", " ", text)

    # trim leading and trailing spaces
    return text.strip()

