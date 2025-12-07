from models import get_zero_shot_classifier

# load zero-shot classification pipeline once for efficiency
zsPipeline = get_zero_shot_classifier()

# emotion categories for journaling context (single-label classification)
labels = ["Positive", "Negative", "Stressed", "Anxious", "Confused", "Excited", "Angry", "Neutral"]
def classify_text(cleaned_text):
    """
    Use a zero-shot transformer model (BART MNLI) to assign an emotion label.
    - The model compares the text against predefined candidate labels.
    - multi_label=False makes sure that only the highest-scoring label is returned and not multiple labels.
    """
    result = zsPipeline(
        cleaned_text,
        candidate_labels=labels,
        multi_label=False, 
    )
    
    # Return the top predicted label
    return result["labels"][0]
