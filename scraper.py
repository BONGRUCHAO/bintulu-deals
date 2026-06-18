import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_econsave():
    url = "https://www.syioknya.com/location/outlet/econsave/econsave-bintulu"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    deals = []

    for item in soup.select("h5"):
        text = item.get_text(strip=True)
        if "Promotion" in text or "Sale" in text:
            deals.append({
                "title": text,
                "source": "Econsave",
                "time": str(datetime.now())
            })

    return deals


def run():
    all_deals = []
    all_deals += fetch_econsave()

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(all_deals, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run()
