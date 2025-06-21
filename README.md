# SpamSheild---Your-AI-Powered-Email-Security-Assistant-

# 🛡️ SpamShield - AI Email Spam + Phishing Detector

SpamShield is a Streamlit-powered web app that connects securely to your Gmail inbox and uses AI to detect both spam and **phishing** emails — offering insights, alerts, and a mini dashboard.

## 🚀 Features

- 🔍 Detects spam emails using a trained ML model (Naive Bayes + TF-IDF)
- 🔐 Scans for phishing threats based on suspicious keywords and links
- 📊 Visual dashboard showing spam & phishing statistics
- 🧠 Explainable results: see which keywords triggered the detection
- ✅ Works with Gmail securely via App Passwords

---

## 🧰 Built With

- Python 3
- Streamlit (for UI)
- scikit-learn (ML model)
- IMAP for Gmail email access
- Regex for phishing analysis

---

## 📥 How to Use

### 🔐 1. Enable 2-Step Verification in Gmail

1. Go to [Google Account Security Settings](https://myaccount.google.com/security)
2. Turn on **2-Step Verification**

### 🔑 2. Create an App Password

1. After 2FA is set up, go to **App Passwords**  
   [Direct Link →](https://myaccount.google.com/apppasswords)
2. Choose **Mail** as the app, and **Other (Custom)** or **Windows Computer**
3. Click **Generate**
4. Copy the 16-character password Google gives you

You will use this App Password (not your real Gmail password) in the app.

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/spamshield.git
cd spamshield

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

#How to run
python train_model.py

python -m streamlit run main.py




