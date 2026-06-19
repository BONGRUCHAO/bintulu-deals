import requests
from bs4 import BeautifulSoup
import json
import os
import subprocess

URL = "https://mbasic.facebook.com/ccfreshwholesale"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

posts = soup.find_all("div", {"data-ft": True})

new_deals = []

for post in posts[:5]:
    text = post.get_text(separator=" ", strip=True)

    if len(text) > 20:
        new_deals.append({
            "title": text[:120]
        })


if not os.path.exists("data.json"):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump([], f)

# 对比
if new_deals != old_deals:

    print("发现新优惠")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(new_deals, f, ensure_ascii=False, indent=2)

    subprocess.run(["python", "send_push.py"])

else:
    print("没有新优惠")
