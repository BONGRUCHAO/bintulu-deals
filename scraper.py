import json
from datetime import datetime

def run():

    deals = [
        {
            "title": "Econsave Weekend Sale - RM1 Deals",
            "time": str(datetime.now())
        },
        {
            "title": "Emart Bintulu Fresh Discount Up To 30%",
            "time": str(datetime.now())
        }
    ]

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run()
