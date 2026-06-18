import json

deals = [
    {"title": "TEST Econsave Sale"},
    {"title": "TEST Emart Promo"}
]

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(deals, f, ensure_ascii=False, indent=2)
