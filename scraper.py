import json
import os
import subprocess

# ====== 1. 模拟抓取新数据 ======
# 以后这里改成真实抓网页逻辑
new_deals = [
    {"title": "TEST Econsave Sale"},
    {"title": "TEST Emart Promo"}
]

# ====== 2. 读取旧数据 ======
if os.path.exists("data.json"):
    with open("data.json", "r", encoding="utf-8") as f:
        old_deals = json.load(f)
else:
    old_deals = []

# ====== 3. 对比新旧 ======
if new_deals != old_deals:

    print("发现新优惠，更新 data.json")

    # 写入新数据
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(new_deals, f, ensure_ascii=False, indent=2)

    # 触发推送
    subprocess.run(["python", "send_push.py"])

else:
    print("没有新优惠")
