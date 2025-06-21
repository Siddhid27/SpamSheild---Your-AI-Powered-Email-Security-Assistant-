import streamlit as st
from app.spam_detector import SpamDetector
from app.email_reader import fetch_emails
from app.phishing_detector import PhishingDetector

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
                phish_detector = PhishingDetector()

                total = len(emails)
                spam_count = 0
                phishing_count = 0
                results = []

                for idx, mail in enumerate(emails):
                    st.markdown(f"### 📩 Email {idx+1}")
                    st.write(f"**From:** {mail['from']}")
                    st.write(f"**Subject:** {mail['subject']}")
                    st.code(mail['body'][:500])

                    # 🔍 Spam Detection with Threshold Rule
                    pred, prob = detector.predict(mail['body'])
                    forced_spam = prob < 0.20
                    final_pred = 1 if (pred == 1 or forced_spam) else 0
                    is_verified = detector.is_verified_sender(mail["from"])

                    if final_pred == 1:
                        label = "🚫 SPAM" if not forced_spam else "⚠️ Possibly Spam"
                        st.error(f"{label} (Confidence: {prob:.2%})")
                        spam_count += 1
                    else:
                        st.success(f"✅ Not Spam (Confidence: {prob:.2%})")

                    if is_verified:
                      st.info("✅ Sender is verified and trusted.")
                    
                    # 🔐 Phishing Detection
                    phish_result = phish_detector.detect(mail['body'])
                    if phish_result["phishing"]:
                        phishing_count += 1

                    with st.expander("🔐 Phishing Alert", expanded=phish_result["phishing"]):
                        if phish_result["phishing"]:
                            st.warning("⚠️ **Potential Phishing Detected!**")
                            st.markdown(f"🧮 **Phishing Score:** `{phish_result['score']}`")

                            if phish_result["keywords"]:
                                st.markdown("🔑 **Suspicious Keywords Found:**")
                                for word in phish_result["keywords"]:
                                    st.code(word)

                            if phish_result["urls"]:
                                st.markdown("🔗 **Suspicious URLs/Links Found:**")
                                for url in phish_result["urls"]:
                                    st.code(url)
                        else:
                            st.success("✅ No phishing indicators detected.")

                    # Final hybrid flag
                    final_spam = (pred == 1) or forced_spam or phish_result["phishing"]

                    results.append({
                        "From": mail["from"],
                        "Subject": mail["subject"],
                        "Spam/Phish": "Yes" if final_spam else "No",
                        "Spam Confidence (%)": round(prob * 100, 2),
                        "Phishing Score": phish_result['score']
                    })

                # 📊 Inbox Summary Dashboard
                st.markdown("## 📊 Inbox Summary")
                st.metric("📩 Total Emails Scanned", total)
                st.metric("🚫 Spam Detected", spam_count)
                st.metric("⚠️ Spam Percentage", f"{(spam_count / total) * 100:.2f}%" if total > 0 else "0.00%")
                st.metric("🔐 Phishing Alerts", phishing_count)

                if st.checkbox("📄 Show Classification Table"):
                    st.dataframe(results)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
else:
    st.info("Enter your email credentials in the sidebar to begin.")
