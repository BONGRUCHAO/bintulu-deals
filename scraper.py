import os
import json
import feedparser
import subprocess

# ===== 1️⃣ 所有超市配置 (加新超市就加在这里) =====
MARKETS = [
    {
        "name": "CC Fresh",
        "source": "ccfresh",
        "rss": "https://rss.app/feeds/pCThJgjEUu66piOP.xml"
    },
    {
        "name": "Boulevard",
        "source": "boulevard",
        "rss": "https://rss.app/feeds/S2EAqffxEjE6oxIb.xml"
    },
    {
        "name": "Everwin Supermarket",
        "source": "everwin",
        "rss": "https://rss.app/feeds/B1pSp0iESHPUG4bx.xml"
    },
    {
        "name": "Emart Malaysia",
        "source": "emart",
        "rss": "https://rss.app/feeds/r7BYJWNSeomvfdiT.xml"
    },
    {
        "name": "MDS",
        "source": "mds",
        "rss": "https://rss.app/feeds/KWh3CyqCRwzQeGnl.xml"
    }
]

# ===== ✅ 三语促销关键词 (中/英/马来) =====
PROMO_KEYWORDS = [
    # 马来文
    "promosi", "jualan", "harga", "murah", "jimat", "diskaun",
    "hari ahli", "ahli", "stok terhad", "hujung minggu", "weekend",
    # 中文
    "促销", "优惠", "特价", "打折", "会员日", "买一送一",
    # 英文
    "sale", "promo", "discount", "special", "offer", "deal",
    # 价格
    "rm", "price", "cashback"
]

# 核心价格词 (必须包含至少一个，确保是促销而非普通公告)
IMPORTANT_PRICE_WORDS = ["rm", "harga", "price", "特价", "折扣"]

def is_promo(text):
    if not text:
        return False
    text_lower = text.lower()
    
    # 必须包含价格相关词
    if not any(word in text_lower for word in IMPORTANT_PRICE_WORDS):
        return False
    
    # 并且至少匹配 2 个通用促销词
    match_count = sum(1 for kw in PROMO_KEYWORDS if kw in text_lower)
    return match_count >= 2

new_deals = []

print(f"🚀 开始监控 {len(MARKETS)} 家超市...")

for market in MARKETS:
    print(f"\n📢 正在检查 {market['name']}...")
    
    try:
        feed = feedparser.parse(market['rss'])
        
        # 取最新 10 条进行筛选
        for entry in feed.entries[:10]:
            title = entry.title or ""
            summary = entry.summary or ""
            content = title + " " + summary
            
            # 🔍 过滤逻辑
            if not is_promo(content):
                continue
            
            # 获取图片
            image_url = None
            if "media_content" in entry:
                try:
                    image_url = entry.media_content[0]["url"]
                except:
                    pass
            
            new_deals.append({
                "market": market["name"],
                "source": market["source"],
                "title": title,
                "link": entry.link,
                "image": image_url,
                "date": entry.get("published", "")
            })
            
            print(f"   ✅ 保留: {title[:40]}...")

    except Exception as e:
        print(f"   ❌ {market['name']} 抓取失败: {e}")

print(f"\n✨ 总共找到 {len(new_deals)} 条有效优惠")

# ===== 2️⃣ 写入 data.json =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data.json")

old_deals = []
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        old_deals = json.load(f)

if new_deals != old_deals:
    print("✅ 发现新优惠，更新 data.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_deals, f, ensure_ascii=False, indent=2)
    
    # 推送通知
    try:
        subprocess.run(["python", "send_push.py"])
    except Exception as e:
        print(f"⚠️ 推送发送失败: {e}")
else:
    print("💤 无新变化，跳过更新")
