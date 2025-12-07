import json
import os
from core.parser import clean_text
from core.classifier import classify_text

class MockPipeline:
    def __call__(self, text, candidate_labels, multi_label):
        text_lower = text.lower()
        
        if "crushing it" in text_lower or "crushing it at" in text_lower:
            return {"labels": ["Positive"], "scores": [0.95]}
        elif "crushing me" in text_lower or "crushing" in text_lower:
            return {"labels": ["Negative"], "scores": [0.90]}
        
        if "killing it" in text_lower:
            return {"labels": ["Positive"], "scores": [0.92]}
        elif "killing me" in text_lower:
            return {"labels": ["Stressed"], "scores": [0.88]}
        
        if "dying to" in text_lower:
            return {"labels": ["Excited"], "scores": [0.85]}
        elif "dying from" in text_lower:
            return {"labels": ["Stressed"], "scores": [0.87]}
        
        if text_lower == "that's sick" or "that is sick" in text_lower:
            return {"labels": ["Positive"], "scores": [0.80]}
        elif "feel sick" in text_lower:
            return {"labels": ["Negative"], "scores": [0.93]}
        
        return {"labels": ["Neutral"], "scores": [0.70]}


def test_ambiguous_phrases(monkeypatch):
    monkeypatch.setattr("core.classifier.zsPipeline", MockPipeline())
    
    positive_crushing = clean_text("I am crushing it at work")
    negative_crushing = clean_text("The workload is crushing me")
    
    assert classify_text(positive_crushing) == "Positive", \
        "Should classify 'crushing it' as Positive"
    assert classify_text(negative_crushing) == "Negative", \
        "Should classify 'crushing me' as Negative"
    
    positive_killing = clean_text("I'm killing it today!")
    negative_killing = clean_text("This deadline is killing me")
    
    assert classify_text(positive_killing) == "Positive", \
        "Should classify 'killing it' as Positive"
    assert classify_text(negative_killing) == "Stressed", \
        "Should classify 'killing me' as Stressed"


def test_empty_string_handling(monkeypatch):
    monkeypatch.setattr("core.classifier.zsPipeline", MockPipeline())
    
    assert classify_text("") == "Neutral", "Empty string should return Neutral"
    assert classify_text("   ") == "Neutral", "Whitespace-only should return Neutral"


def test_ambiguous_entries_from_file(monkeypatch):
    monkeypatch.setattr("core.classifier.zsPipeline", MockPipeline())
    
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "ambiguous_entries.json")
    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            test_cases = json.load(f)
        
        for case in test_cases:
            cleaned = clean_text(case["text"])
            result = classify_text(cleaned)
            assert result in ["Positive", "Negative", "Stressed", "Anxious", "Confused", "Excited", "Angry", "Neutral"], \
                f"Classification result '{result}' should be a valid emotion label"

