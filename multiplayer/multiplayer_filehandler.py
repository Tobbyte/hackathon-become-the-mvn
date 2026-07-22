import json


def save_file(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as file_w:
        json.dump(data, file_w, indent=4)


def load_file(filename: str) -> dict:  # waht ahppens with the timestamp?
    with open(filename, "r", encoding="utf-8") as file_r:
        data = json.load(file_r)
        return data
