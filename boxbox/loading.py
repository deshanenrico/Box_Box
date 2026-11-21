import json
import pandas as pd


def load_json(filepath):
    """
    Load a JSON file and return its contents.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data