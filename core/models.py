from transformers import pipeline 

def get_zero_shot_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )
