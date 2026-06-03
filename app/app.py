from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import os
import json

app = Flask(__name__)

# Enable CORS for Chrome Extension
CORS(app)

# ==========================
# Load Model
# ==========================

model = joblib.load("../model/model.pkl")
vectorizer = joblib.load("../model/vectorizer.pkl")

HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

# ==========================
# Save History
# ==========================

def save_history(entry):
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================
# Website Prediction
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    email_text = request.form["email"]

    vec = vectorizer.transform([email_text])

    prediction = model.predict(vec)[0]
    confidence = float(model.predict_proba(vec)[0][1] * 100)

    phishing_keywords = [
        "urgent",
        "verify",
        "password",
        "click",
        "bank",
        "account",
        "suspend",
        "login"
    ]

    suspicious = any(
        word in email_text.lower()
        for word in phishing_keywords
    )

    has_link = (
        "http" in email_text.lower()
        or
        "www" in email_text.lower()
    )

    reasons = []

    if suspicious:
        reasons.append("Contains phishing keywords")

    if has_link:
        reasons.append("Contains suspicious link")

    if confidence > 80:
        reasons.append("High model confidence")

    if prediction == 1 or (suspicious and has_link):
        result = "🚨 Phishing Email"
        risk = "High"
        color = "red"
    else:
        result = "✅ Safe Email"
        risk = "Low"
        color = "green"

    save_history({
        "text": email_text[:100],
        "result": result,
        "confidence": round(confidence, 2)
    })

    return render_template(
        "index.html",
        result=result,
        confidence=round(confidence, 2),
        risk=risk,
        color=color,
        reasons=reasons
    )

# ==========================
# Browser Extension API
# ==========================

@app.route("/api/predict", methods=["POST"])
def api_predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        email_text = data.get("email", "")

        vec = vectorizer.transform([email_text])

        prediction = model.predict(vec)[0]
        confidence = float(model.predict_proba(vec)[0][1] * 100)

        phishing_keywords = [
            "urgent",
            "verify",
            "password",
            "click",
            "bank",
            "account",
            "suspend",
            "login"
        ]

        suspicious = any(
            word in email_text.lower()
            for word in phishing_keywords
        )

        has_link = (
            "http" in email_text.lower()
            or
            "www" in email_text.lower()
        )

        reasons = []

        if suspicious:
            reasons.append("Contains phishing keywords")

        if has_link:
            reasons.append("Contains suspicious link")

        if confidence > 80:
            reasons.append("High model confidence")

        if prediction == 1 or (suspicious and has_link):
            result = "Phishing Email"
            risk = "High"
        else:
            result = "Safe Email"
            risk = "Low"

        save_history({
            "text": email_text[:100],
            "result": result,
            "confidence": round(confidence, 2)
        })

        return jsonify({
            "result": result,
            "risk": risk,
            "confidence": round(confidence, 2),
            "reasons": reasons
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    total = len(data)

    phishing = len([
        x for x in data
        if "Phishing" in x["result"]
    ])

    safe = total - phishing

    return render_template(
        "dashboard.html",
        data=data[::-1],
        total=total,
        phishing=phishing,
        safe=safe
    )

# ==========================
# Run App
# ==========================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )