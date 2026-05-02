from flask import Flask, render_template, request
import pickle
import os
import json

app = Flask(__name__)

# Load model
model = pickle.load(open("../model/model.pkl", "rb"))
vectorizer = pickle.load(open("../model/vectorizer.pkl", "rb"))

HISTORY_FILE = "history.json"

# Create history file if not exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


def save_history(entry):
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["email"]

    # ML prediction
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0][1] * 100

    # 🔥 Hybrid rule-based detection (FIXED)
    phishing_keywords = [
        "urgent", "verify", "password", "click",
        "bank", "account", "suspend", "login"
    ]

    suspicious = any(word in text.lower() for word in phishing_keywords)
    has_link = "http" in text or "www" in text

    if pred == 1 or (suspicious and has_link):
        result = "🚨 Phishing Email"
        risk = "High"
        color = "red"
    else:
        result = "✅ Safe Email"
        risk = "Low"
        color = "green"

    # Explanation system
    reasons = []

    if suspicious:
        reasons.append("Contains phishing keywords")

    if has_link:
        reasons.append("Contains suspicious link")

    if prob > 80:
        reasons.append("Model highly confident")

    # Save history
    save_history({
        "text": text,
        "result": result,
        "confidence": round(prob, 2)
    })

    return render_template(
        "index.html",
        result=result,
        confidence=round(prob, 2),
        risk=risk,
        color=color,
        reasons=reasons
    )


@app.route("/dashboard")
def dashboard():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    total = len(data)
    phishing = len([x for x in data if "Phishing" in x["result"]])
    safe = total - phishing

    return render_template(
        "dashboard.html",
        data=data[::-1],
        total=total,
        phishing=phishing,
        safe=safe
    )


if __name__ == "__main__":
    app.run(debug=True)