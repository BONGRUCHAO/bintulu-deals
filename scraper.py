import requests
from bs4 import BeautifulSoup
import json
import os
import subprocess

URL = "https://mbasic.facebook.com/ccfreshwholesale"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}

try:
    print(f"正在请求: {URL}")
    response = requests.get(URL, headers=headers, timeout=15)
    print(f"状态码: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", {"data-ft": True})
    print(f"找到帖子数量: {len(posts)}")

    new_deals = []
    for post in posts[:5]:
        text = post.get_text(separator=" ", strip=True)
        if len(text) > 10:
            new_deals.append({"title": text[:120]})

    # --- ⭐️ 关键修改开始 ⭐️ ---
    
    # 1. 强制检查：如果文件不存在，直接创建它（即使是空的）
    if not os.path.exists("data.json"):
        print("首次运行：强制创建 data.json")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(new_deals, f, ensure_ascii=False, indent=2)
        # 强制触发一次提交
        subprocess.run(["python", "send_push.py"])
        exit(0) # 退出，交给 Git 处理

    # 2. 如果文件存在，再进行对比
    with open("data.json", "r", encoding="utf-8") as f:
        try:
            old_deals = json.load(f)
        except:
            old_deals = []

    if new_deals != old_deals:
        print("✅ 发现新优惠，更新 data.json")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(new_deals, f, ensure_ascii=False, indent=2)
        subprocess.run(["python", "send_push.py"])
    else:
        print("💤 数据没有变化，无需更新")

    # --- ⭐️ 关键修改结束 ⭐️ ---

except Exception as e:
    print(f"🚨 错误: {e}")
