import imaplib
import email
from email.header import decode_header
from datetime import datetime
from bs4 import BeautifulSoup

def clean_email_body(raw_body):
    soup = BeautifulSoup(raw_body, "html.parser")
    text = soup.get_text(separator=" ")
    return text.strip()

def fetch_emails(user, password, num_emails=10):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, password)
    imap.select("inbox")

    # Fetch all email IDs
    status, message_numbers = imap.search(None, "ALL")
    message_numbers = message_numbers[0].split()

    # Limit to latest 30 for speed
    recent_ids = message_numbers[-30:]

    # Get dates for sorting
    email_dates = []
    for msg_id in recent_ids:
        typ, msg_data = imap.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (DATE)])')
        raw_date = email.message_from_bytes(msg_data[0][1])["Date"]
        try:
            date_obj = email.utils.parsedate_to_datetime(raw_date)
        except Exception:
            date_obj = datetime.min
        email_dates.append((msg_id, date_obj))

    # Sort by most recent
    sorted_ids = sorted(email_dates, key=lambda x: x[1], reverse=True)
    final_ids = [item[0] for item in sorted_ids[:num_emails]]

    emails = []
    for mail_id in final_ids:
        status, msg_data = imap.fetch(mail_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_header(msg["Subject"])[0][0]
                subject = subject.decode() if isinstance(subject, bytes) else subject
                from_ = msg.get("From")
                date = msg.get("Date")

                body = ""
                html_body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        if ctype == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        elif ctype == "text/html" and "attachment" not in str(part.get("Content-Disposition")):
                            html_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                else:
                    ctype = msg.get_content_type()
                    if ctype == "text/plain":
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    elif ctype == "text/html":
                        html_body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                # Use plain text if available, else clean HTML
                final_body = body if body else clean_email_body(html_body)

                emails.append({
                    'from': from_,
                    'subject': subject,
                    'body': final_body,
                    'date': date
                })

    imap.logout()
    return emails
