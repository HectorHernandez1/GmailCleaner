# gmail_mcp.py  
# A simple Python MCP connector for Gmail cleanup operations: delete and flag emails.
# Uses FastAPI for HTTP endpoints and google-api-python-client for Gmail API.

import os
import re
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Configuration ---
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
]
CLIENT_SECRETS_FILE = 'credentials.json'  # Download from Google Cloud Console
TOKEN_FILE = 'token.json'                 # Will be created by OAuth flow

# --- Initialize Gmail service ---
creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

gmail = build('gmail', 'v1', credentials=creds)

# --- FastAPI app ---
app = FastAPI()

class MCPRequest(BaseModel):
    input: dict
    config: dict = {}

class MCPResponse(BaseModel):
    output: dict

@app.get("/info")
def info():
    return {
        "name": "gmail-cleaner",
        "description": "Clean up Gmail: delete messages, flag/star messages based on instructions.",
        "actions": ["delete", "flag"],
        "version": "0.1.0"
    }

@app.post("/run", response_model=MCPResponse)
async def run(req: MCPRequest):
    user_input = req.input.get("content", "")

    # Simple parsing: look for keywords delete or flag and a message ID or query
    if 'delete' in user_input.lower():
        # e.g., "delete email with subject Invoice"
        query = extract_query(user_input)
        ids = search_messages(query)
        for mid in ids:
            gmail.users().messages().delete(userId='me', id=mid).execute()
        return MCPResponse(output={"response": f"Deleted {len(ids)} messages matching '{query}'"})

    elif 'flag' in user_input.lower() or 'star' in user_input.lower():
        query = extract_query(user_input)
        ids = search_messages(query)
        for mid in ids:
            gmail.users().messages().modify(
                userId='me', id=mid,
                body={"addLabelIds": ["STARRED"]}
            ).execute()
        return MCPResponse(output={"response": f"Flagged {len(ids)} messages matching '{query}'"})

    else:
        raise HTTPException(status_code=400, detail="Unsupported action. Use 'delete' or 'flag'.")

# --- Helper functions ---
def extract_query(text: str) -> str:
    # crude: extract after 'subject', 'from', or full-body
    m = re.search(r"subject\s+(.*)", text, re.IGNORECASE)
    return m.group(1) if m else text


def search_messages(query: str):
    # Use Gmail API to search messages
    result = gmail.users().messages().list(userId='me', q=query).execute()
    msgs = result.get('messages', [])
    return [m['id'] for m in msgs]

# --- Run with: uvicorn gmail_mcp:app --host 0.0.0.0 --port 8080 ---
