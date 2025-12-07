from core.classifier import classify_text

class FakePipeline:
    def __call__(self, text, candidate_labels, multi_label):
        return {"labels": ["Positive"], "scores": [0.99]}

def test_classification(monkeypatch):
    monkeypatch.setattr("core.classifier.zsPipeline", FakePipeline())
    assert classify_text("i feel great") == "Positive"

def test_empty_string_handling(monkeypatch):
    monkeypatch.setattr("core.classifier.zsPipeline", FakePipeline())
    assert classify_text("") == "Neutral"
    assert classify_text("   ") == "Neutral"