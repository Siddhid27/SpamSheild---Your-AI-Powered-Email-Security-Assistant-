import re

SUSPICIOUS_KEYWORDS = [
    "verify", "update your account", "click here", "reset password",
    "login attempt", "unauthorized", "suspended", "limited access",
    "OTP", "account locked", "bank info", "urgent", "confirm now"
]

SUSPICIOUS_DOMAINS = [
    "bit.ly", "tinyurl", "ow.ly", "grabify", "adf.ly"
]

class PhishingDetector:
    def __init__(self):
        self.keyword_patterns = [re.compile(rf"\b{k}\b", re.IGNORECASE) for k in SUSPICIOUS_KEYWORDS]
        self.domain_patterns = [re.compile(d) for d in SUSPICIOUS_DOMAINS]

    def detect(self, text):
        keyword_hits = [k.pattern for k in self.keyword_patterns if k.search(text)]
        url_hits = [d.pattern for d in self.domain_patterns if d.search(text)]

        score = len(keyword_hits) + len(url_hits)

        return {
            "phishing": score > 1,
            "keywords": keyword_hits,
            "urls": url_hits,
            "score": score
        }
