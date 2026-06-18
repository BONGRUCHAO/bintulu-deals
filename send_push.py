import json
from pywebpush import webpush

PUBLIC_KEY = "你的公钥"
PRIVATE_KEY = "你的私钥"


def send_all(title, body):

    try:
        with open(
            "subs.json",
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                sub = json.loads(line)

                webpush(
                    subscription_info=sub,
                    data=json.dumps({
                        "title": title,
                        "body": body
                    }),
                    vapid_private_key=PRIVATE_KEY,
                    vapid_claims={
                        "sub":"mailto:test@test.com"
                    }
                )

    except:
        pass
