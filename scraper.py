import os
import json
import feedparser
import subprocess

# ===== 1️⃣ RSS 地址 =====
RSS_URL = "https://rss.app/feeds/pCThJgjEUu66piOP.xml"

print("正在请求 RSS 源:", RSS_URL)

feed = feedparser.parse(RSS_URL)

# ===== ✅ 促销关键词 =====
PROMO_KEYWORDS = [
    "促销", "特价", "优惠", "打折", "减价",
    "会员日", "会员价", "会员专享",
    "特卖", "清仓", "限时", "买一送一",
    "RM", "令吉",
    "sale", "promo", "promotion",
    "discount", "offer", "deal",
    "member day", "member only"
]

def is_promo(text):
    if not text:
        return False

    text_lower = text.lower()
    for keyword in PROMO_KEYWORDS:
        if keyword.lower() in text_lower:
            return True
    return False


new_deals = []

# ✅ 多抓几条，然后筛选
for entry in feed.entries[:10]:

    title = entry.title or ""
    summary = entry.summary or ""
    content = title + " " + summary

    # ⭐️ 过滤非促销内容
    if not is_promo(content):
        print("跳过(非促销):", title[:40])
        continue

    image_url = None
    if "media_content" in entry:
        try:
            image_url = entry.media_content[0]["url"]
        except:
            pass

    new_deals.append({
        "title": title,
        "link": entry.link,
        "image": image_url
    })

    print("✅ 保留:", title[:40])

print("最终保留", len(new_deals), "条促销信息")

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

    # 推送（失败不影响提交）
    try:
        subprocess.run(["python", "send_push.py"])
    except Exception as e:
        print("Push 发送失败:", e)

else:
    print("没有新促销，不更新文件")
