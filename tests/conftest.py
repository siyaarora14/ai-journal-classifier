import sys
import os

# determine the project root directory
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# add that directory to Python's import path so core/ and storage/ can be imported 
sys.path.insert(0, ROOT)
