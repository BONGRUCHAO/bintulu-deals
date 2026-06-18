from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    return render_template("index.html", deals=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
