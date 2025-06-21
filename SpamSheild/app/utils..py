import streamlit as st
from app.spam_detector import SpamDetector
from app.email_reader import fetch_emails

st.set_page_config(page_title="📧 SpamShield", layout="centered")
st.title("🛡️ SpamShield: AI Email Spam Detector")

with st.sidebar:
    st.header("📥 Email Login")
    user_email = st.text_input("Your Email (Gmail)", value="", placeholder="you@gmail.com")
    password = st.text_input("App Password", value="", type="password")

if user_email and password:
    if st.button("🔍 Fetch & Check Emails"):
        with st.spinner("Fetching emails..."):
            try:
                emails = fetch_emails(user_email, password)
                detector = SpamDetector()

                for idx, mail in enumerate(emails):
                    st.markdown(f"### 📩 Email {idx+1}")
                    st.write(f"**From:** {mail['from']}")
                    st.write(f"**Subject:** {mail['subject']}")
                    st.code(mail['body'][:500])

                    pred, prob = detector.predict(mail['body'])
                    if pred == 1:
                        st.error(f"🚫 SPAM (Confidence: {prob:.2%})")
                    else:
                        st.success(f"✅ Not Spam (Confidence: {prob:.2%})")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
else:
    st.info("Enter your email credentials in the sidebar to begin.")
