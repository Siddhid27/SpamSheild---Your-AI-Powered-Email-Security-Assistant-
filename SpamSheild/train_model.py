import pandas as pd
import re
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
df = pd.read_csv("data/mail_data.csv")
df["Category"] = df["Category"].astype(int)

# Features and labels
X = df["Message"]
y = df["Category"]  # 1 = spam, 0 = ham

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", lowercase=True)),
    ("clf", MultinomialNB())
])

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("📊 Model Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("model", exist_ok=True)
with open("model/spam_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved to model/spam_model.pkl")
