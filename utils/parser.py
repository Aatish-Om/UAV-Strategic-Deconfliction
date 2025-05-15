# utils/parser.py
import json

def load_mission(file_path):
    with open(file_path) as f:
        return json.load(f)

