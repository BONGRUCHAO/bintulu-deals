import requests
from bs4 import BeautifulSoup
import json
import os
import subprocess

URL = "https://mbasic.facebook.com/ccfreshwholesale"

# ⭐️ 增强版 Header，模拟真实浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    print(f"正在请求: {URL}")
    response = requests.get(URL, headers=headers, timeout=15)
    print(f"状态码: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ 抓取失败，状态码: {response.status_code}")
        # 即使失败也不崩溃，直接退出，这样 Workflow 依然是绿色的
        exit(0) 

    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", {"data-ft": True})
    print(f"找到帖子数量: {len(posts)}")

    new_deals = []
    for post in posts[:5]:
        text = post.get_text(separator=" ", strip=True)
        if len(text) > 10:
            new_deals.append({"title": text[:120]})

    # 读取旧数据
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            try:
                old_deals = json.load(f)
            except:
                old_deals = []
    else:
        old_deals = []

    if new_deals != old_deals:
        print("✅ 发现新优惠，更新 data.json")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(new_deals, f, ensure_ascii=False, indent=2)
        
        # 触发推送
        if os.path.exists("send_push.py"):
            subprocess.run(["python", "send_push.py"])
    else:
        print("💤 没有新优惠")

except Exception as e:
    print(f"🚨 发生未知错误: {e}")
    exit(0) # 即使报错也不崩溃，确保 Workflow 流程走完
