import os
import pickle
import base64
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Gmail:
    def __init__(self, credentials_file='credentials.json'):
        self.credentials_file = credentials_file
        self._generate_credentials_if_needed()
        self.service = self._get_gmail_service()

    def _generate_credentials_if_needed(self):
        if not os.path.exists(self.credentials_file):
            print("credentials.json not found. Generating from .env file...")
            creds_data = {
                "installed": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_URL"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URIS")]
                }
            }
            if not all([creds_data["installed"]["client_id"], creds_data["installed"]["client_secret"]]):
                 raise ValueError("Missing Google credentials in .env file. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.")

            with open(self.credentials_file, 'w') as f:
                json.dump(creds_data, f)
            print("credentials.json generated successfully.")

    def _get_gmail_service(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, ['https://www.googleapis.com/auth/gmail.modify'])
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def search_emails(self, query):
        result = self.service.users().messages().list(userId='me', q=query).execute()
        return result.get('messages', [])

    def trash_email(self, msg_id):
        try:
            self.service.users().messages().trash(userId='me', id=msg_id).execute()
            print(f'Email with id: {msg_id} trashed successfully.')
        except Exception as e:
            print(f'An error occurred: {e}')

    def get_message(self, msg_id):
        return self.service.users().messages().get(userId='me', id=msg_id).execute()

    def get_email_date(self, msg_id):
        msg = self.get_message(msg_id)
        headers = msg['payload']['headers']
        for header in headers:
            if header['name'] == 'Date':
                return header['value']
        return None

    def send_email(self, to, subject, message_html):
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(message_html, 'html'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}
        try:
            message = (self.service.users().messages().send(userId='me', body=body)
                       .execute())
            print(f'Message Id: {message["id"]}')
            return message
        except Exception as e:
            print(f'An error occurred: {e}')