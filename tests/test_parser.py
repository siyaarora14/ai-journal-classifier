from core.parser import clean_text

def test_slang_expansion():
    assert clean_text("idk what to do") == "i don't know what to do"

def test_emoji_conversion():
    assert "sad" in clean_text("i am 😢")

def test_regex_cleanup():
    assert clean_text("hello!!!") == "hello"
