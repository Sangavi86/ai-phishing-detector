# 🛡️ AI Phishing Email Detector

This project is a simple but powerful web app that checks whether an email is **phishing or safe** using Machine Learning.

Instead of manually guessing suspicious emails, this tool analyzes the content and gives a quick prediction along with confidence.

---

## 💡 Why this project?

Phishing attacks are one of the most common cyber threats. Many users can’t easily identify fake emails.

This project solves that problem by:

* Analyzing email text
* Detecting suspicious patterns
* Giving instant results in a user-friendly interface

---

## 🚀 What it can do

* Detect if an email is **Phishing** or **Safe**
* Show prediction with confidence score
* Highlight risky keywords
* Store previous results (history)
* Clean and modern UI for easy use

---

## 🧠 How it works (simple explanation)

1. Email text is given as input
2. Text is cleaned and processed
3. Converted into numerical format using TF-IDF
4. Machine Learning model analyzes it
5. Output is shown as:

   * ✅ Safe
   * ⚠️ Phishing

---

## 🛠️ Tech used

* Python
* Flask (for backend)
* HTML, CSS (for UI)
* Scikit-learn (ML model)
* Pandas & NumPy

---

## 📁 Project structure

```
ai-phishing-detector/
│
├── app/
│   ├── app.py              # Main backend
│   ├── history.json        # Stores previous results
│   └── templates/
│       ├── index.html      # Main UI
│       └── dashboard.html
│
├── data/
│   └── emails.csv          # Dataset
│
├── model/
│   ├── model.pkl           # Trained ML model
│   └── vectorizer.pkl      # Text vectorizer
│
├── train_model.py          # Model training file
└── README.md
```

---

## ⚙️ How to run this project

### Step 1: Clone the repo

```
git clone https://github.com/Sangavi86/ai-phishing-detector.git
cd ai-phishing-detector
```

### Step 2: Install libraries

```
pip install pandas numpy scikit-learn flask
```

### Step 3: Train the model

```
python train_model.py
```

### Step 4: Run the app

```
cd app
python app.py
```

### Step 5: Open browser

```
http://127.0.0.1:5000
```

---

## 🧪 Try these examples

### 🔴 Phishing example

```
URGENT: Your account will be suspended!
Click here to verify immediately: http://fake-link.com
```

### 🟢 Safe example

```
Hi, just checking if you're available for tomorrow's meeting.
```

---

## 📊 Model performance

* Accuracy: ~97%
* Trained on real dataset
* Fast predictions

---

## 🔮 Future improvements

* URL detection system
* Email header analysis
* Deep learning (BERT)
* Cloud deployment
* Better UI animations

---

## 👩‍💻 Author

Sangavi N
GitHub: https://github.com/Sangavi86

---

## ⭐ Final note

This project shows how Machine Learning can be used in real-world cybersecurity problems in a simple and practical way.
