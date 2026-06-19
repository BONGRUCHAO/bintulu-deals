import os
import json
import feedparser
import subprocess

# ===== 1️⃣ RSS 地址 =====
RSS_URL = "https://rss.app/feeds/pCThJgjEUu66piOP.xml"

print("正在请求 RSS 源:", RSS_URL)

feed = feedparser.parse(RSS_URL)

new_deals = []

for entry in feed.entries[:5]:
    new_deals.append({
        "title": entry.title,
        "link": entry.link
    })

print("成功抓取到", len(new_deals), "条优惠")

# ===== 2️⃣ 绝对路径写入 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data.json")

# 读取旧数据
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        old_deals = json.load(f)
else:
    old_deals = []

# 对比
if new_deals != old_deals:

    print("✅ 发现新优惠，更新 data.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_deals, f, ensure_ascii=False, indent=2)

    print("✅ data.json 写入路径:", file_path)

    # ===== 3️⃣ 推送（失败不影响提交）=====
    try:
        subprocess.run(["python", "send_push.py"])
    except Exception as e:
        print("Push 发送失败:", e)

else:
    print("没有新优惠，不更新文件")
