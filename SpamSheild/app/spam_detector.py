import pickle
import os
import pandas as pd

class SpamDetector:
    def __init__(self):
        # Load trained model
        model_path = os.path.join("model", "spam_model.pkl")
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        # Load verified senders CSV from data folder
        whitelist_path = os.path.join("data", "verified_senders.csv")
        if os.path.exists(whitelist_path):
            self.verified_df = pd.read_csv(whitelist_path)
            self.verified_emails = set(self.verified_df['email_domain'].str.lower().tolist())
        else:
            self.verified_emails = set()

    def is_verified_sender(self, email_sender):
        """Check if the sender matches any whitelisted domain."""
        if not email_sender:
            return False
        email_sender = email_sender.lower()
        return any(verified in email_sender for verified in self.verified_emails)

    def predict(self, text):
        pred = self.model.predict([text])[0]
        prob = self.model.predict_proba([text])[0][1]  # Confidence for spam class
        return pred, prob
