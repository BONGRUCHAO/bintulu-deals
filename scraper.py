import feedparser # 需安装
import json
import os
import subprocess

# ⭐️ 替换成你在 RSS.app 申请到的真实链接
RSS_URL = "https://rss.app/feeds/pCThJgjEUu66piOP.xml"

try:
    print(f"正在请求 RSS 源: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    
    new_deals = []
    # 抓取最新的 5 条帖子
    for entry in feed.entries[:5]:
        new_deals.append({
            "title": entry.title[:120], 
            "link": entry.link
        })
    
    print(f"成功抓取到 {len(new_deals)} 条优惠")

    # 读取旧数据
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            try:
                old_deals = json.load(f)
            except:
                old_deals = []
    else:
        old_deals = []

    # 对比并更新
    if new_deals != old_deals:
        print("✅ 发现新优惠，更新 data.json")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(new_deals, f, ensure_ascii=False, indent=2)
        
        if os.path.exists("send_push.py"):
            subprocess.run(["python", "send_push.py"])
    else:
        print("💤 数据没有变化")

except Exception as e:
    print(f"🚨 错误: {e}")
