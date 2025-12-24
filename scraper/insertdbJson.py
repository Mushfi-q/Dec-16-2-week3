import json

with open("books.json", "r", encoding="utf-8") as f:
    all_books = json.load(f)