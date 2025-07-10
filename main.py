from dotenv import load_dotenv
load_dotenv() # Load environment variables first

from gmail import Gmail
from datetime import datetime, timedelta
import os

# --- Configuration Variables ---
# Set the action to perform: "delete-by-sender", "delete-by-age", "send", "delete-from-list", or ""
ACTION = os.getenv("ACTION", "").lower()

# --- Settings for 'delete-by-sender' ---
SENDER_TO_DELETE = os.getenv("SENDER_TO_DELETE")

# --- Settings for 'delete-by-age' ---
DAYS_TO_DELETE = int(os.getenv("DAYS_TO_DELETE", 1095))

# --- Settings for 'send' ---
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")
EMAIL_BODY = os.getenv("EMAIL_BODY")

# --- Settings for 'delete-from-list' ---
EMAIL_LIST_FILE = "emails_to_delete.txt"

def delete_emails_by_sender(gmail):
    """Deletes emails from a specific sender."""
    if not SENDER_TO_DELETE:
        print("SENDER_TO_DELETE is not set. Skipping.")
        return
    print(f"Searching for emails from {SENDER_TO_DELETE}...")
    emails = gmail.search_emails(f'from:{SENDER_TO_DELETE}')
    if not emails:
        print(f"No emails found from {SENDER_TO_DELETE}.")
        return
    print(f"Found {len(emails)} emails. Trashing them...")
    for email in emails:
        gmail.trash_email(email['id'])
    print("Done.")

def delete_emails_by_age(gmail):
    """Deletes emails older than a specified number of days."""
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_DELETE)
    query = f'before:{cutoff_date.strftime("%Y/%m/%d")}'
    print(f"Searching for emails older than {DAYS_TO_DELETE} days (before {cutoff_date.strftime('%Y-%m-%d')})...")
    emails = gmail.search_emails(query)
    if not emails:
        print("No emails found matching the criteria.")
        return
    print(f"Found {len(emails)} emails. Trashing them...")
    for email in emails:
        gmail.trash_email(email['id'])
    print("Done.")

def send_email_action(gmail):
    """Sends an email."""
    if not RECIPIENT_EMAIL:
        print("RECIPIENT_EMAIL is not set. Skipping.")
        return
    print(f"Sending email to {RECIPIENT_EMAIL}...")
    gmail.send_email(RECIPIENT_EMAIL, EMAIL_SUBJECT, EMAIL_BODY)
    print("Email sent.")

def delete_from_list(gmail):
    """Deletes emails from a list of senders in a file."""
    if not os.path.exists(EMAIL_LIST_FILE):
        print(f"Error: {EMAIL_LIST_FILE} not found.")
        return
    
    with open(EMAIL_LIST_FILE, 'r') as f:
        senders = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not senders:
        print(f"No email addresses found in {EMAIL_LIST_FILE}.")
        return

    print(f"Found {len(senders)} email addresses in the list.")
    for sender in senders:
        print(f"\n--- Deleting emails from: {sender} ---")
        delete_emails_by_sender_from_list(gmail, sender)

def delete_emails_by_sender_from_list(gmail, sender):
    """Helper function to delete emails for the list functionality."""
    emails = gmail.search_emails(f'from:{sender}')
    if not emails:
        print(f"No emails found from {sender}.")
        return
    print(f"Found {len(emails)} emails. Trashing them...")
    for email in emails:
        gmail.trash_email(email['id'])
    print(f"Finished deleting emails from {sender}.")

def main():
    gmail = Gmail()

    action = ACTION.lower().strip()
    if action == 'delete-by-sender':
        delete_emails_by_sender(gmail)
    elif action == 'delete-by-age':
        delete_emails_by_age(gmail)
    elif action == 'send':
        send_email_action(gmail)
    elif action == 'delete-from-list':
        delete_from_list(gmail)
    else:
        print(f"No action or invalid action specified. Please set ACTION in the .env file.")

if __name__ == "__main__":
    main()
