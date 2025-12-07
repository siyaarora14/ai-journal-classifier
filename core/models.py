%pip install -q transformers
from transformers import pipeline 
from pprint import pprint
classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli")
