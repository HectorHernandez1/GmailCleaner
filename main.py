from gmail import Gmail
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

def delete_old_emails(gmail):
    three_years_ago = datetime.now() - timedelta(days=3*365)
    query = f'before:{three_years_ago.strftime("%Y/%m/%d")}'
    emails = gmail.search_emails(query)
    if not emails:
        print("No emails found older than 3 years.")
    else:
        for email in emails:
            gmail.trash_email(email['id'])

def main():
    gmail = Gmail()
    
    # Delete emails from a specific sender
    sender_to_delete = os.getenv("SENDER_TO_DELETE")
    if sender_to_delete:
        emails = gmail.search_emails(f'from:{sender_to_delete}')
        if not emails:
            print(f"No emails found from {sender_to_delete}.")
        else:
            for email in emails:
                gmail.trash_email(email['id'])

    # Delete emails older than 3 years
    delete_old_emails(gmail)

    # Example of sending an email with HTML content
    recipient = "recipient@example.com"
    subject = "Hello from Gemini!"
    html_body = """
    <html>
        <body>
            <p style="font-family: sans-serif; font-size: 14px; color: #333;">This is a test email sent from the Gmail Cleaner script.</p>
            <p style="font-family: Georgia, serif; font-size: 16px; color: #0055a5; font-weight: bold;">You can use any HTML and CSS to style your email!</p>
        </body>
    </html>
    """
    gmail.send_email(recipient, subject, html_body)

if __name__ == "__main__":
    main()