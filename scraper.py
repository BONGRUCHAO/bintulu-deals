import os
import json
import feedparser
import subprocess
from bs4 import BeautifulSoup

# =====================================================
# 🏬 所有超市配置
# =====================================================
MARKETS = [
    {"name": "CC Fresh", "source": "ccfresh", "rss": "https://rss.app/feeds/pCThJgjEUu66piOP.xml"},
    {"name": "Boulevard", "source": "boulevard", "rss": "https://rss.app/feeds/S2EAqffxEjE6oxIb.xml"},
    {"name": "Doremart", "source": "doremart", "rss": "https://rss.app/feeds/bRBqDaUPXCqH9QIu.xml"},
    {"name": "New World Mart", "source": "newworld", "rss": "https://rss.app/feeds/mcY7198sT4xcZPc1.xml"},
    {"name": "Farley", "source": "farley", "rss": "https://rss.app/feeds/cjYeT5rh0Ajauosn.xml"},
    {"name": "Econsave", "source": "econsave", "rss": "https://rss.app/feeds/T3CJJciCuuTdZU8b.xml"},
    {"name": "SING KWONG", "source": "singkwong", "rss": "https://rss.app/feeds/KxuEBW2965BgMH3l.xml"},
    {"name": "Everwin Supermarket", "source": "everwin", "rss": "https://rss.app/feeds/B1pSp0iESHPUG4bx.xml"},
    {"name": "Emart Malaysia", "source": "emart", "rss": "https://rss.app/feeds/r7BYJWNSeomvfdiT.xml"},
    {"name": "MDS", "source": "mds", "rss": "https://rss.app/feeds/KWh3CyqCRwzQeGnl.xml"},
]

# =====================================================
# 🔎 三语促销关键词
# =====================================================
PROMO_KEYWORDS = [
    # 马来
    "promosi", "jualan", "harga", "murah", "jimat",
    "diskaun", "ahli", "hujung minggu", "weekend",

    # 中文
    "促销", "优惠", "特价", "会员日", "买一送一",

    # 英文
    "sale", "promo", "discount", "offer", "deal",

    # 价格
    "rm", "price"
]

IMPORTANT_PRICE_WORDS = ["rm", "harga", "price", "特价"]

def is_promo(text):
    if not text:
        return False

    text_lower = text.lower()

    # 必须包含价格相关词
    if not any(word in text_lower for word in IMPORTANT_PRICE_WORDS):
        return False

    # 至少匹配 2 个关键词
    match_count = sum(1 for kw in PROMO_KEYWORDS if kw in text_lower)
    return match_count >= 2


# =====================================================
# 🚀 开始抓取
# =====================================================
new_deals = []
seen_titles = set()

print(f"🚀 开始监控 {len(MARKETS)} 家超市...")

for market in MARKETS:
    print(f"\n📢 正在检查 {market['name']}...")

    try:
        feed = feedparser.parse(market["rss"])

        for entry in feed.entries[:10]:
            title = entry.title or ""
            summary = entry.summary or ""
            content = title + " " + summary

            if not is_promo(content):
                continue

            if title in seen_titles:
                continue

            seen_titles.add(title)

            # ✅ 多图支持
            images = []

            # 1️⃣ media_content
            if "media_content" in entry:
                try:
                    for media in entry.media_content:
                        if "url" in media:
                            images.append(media["url"])
                except:
                    pass

            # 2️⃣ 从 summary 里解析图片
            if not images and summary:
                soup = BeautifulSoup(summary, "html.parser")
                for img in soup.find_all("img"):
                    images.append(img.get("src"))

            # 去重
            images = list(dict.fromkeys(images))

            new_deals.append({
                "market": market["name"],
                "source": market["source"],
                "title": title,
                "link": entry.link,
                "images": images,
                "date": entry.get("published", "")
            })

            print(f"   ✅ 保留: {title[:40]}")

    except Exception as e:
        print(f"   ❌ {market['name']} 抓取失败: {e}")

print(f"\n✨ 总共找到 {len(new_deals)} 条有效优惠")


# =====================================================
# 💾 写入 data.json
# =====================================================
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

    try:
        subprocess.run(["python", "send_push.py"])
    except Exception as e:
        print(f"⚠️ 推送发送失败: {e}")
else:
    print("💤 无新变化，跳过更新")
