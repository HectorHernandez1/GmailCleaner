# Gmail Cleaner

This Python script helps you manage your Gmail inbox by providing functionalities to clean up emails based on specific criteria and to send emails. It is configured via a `.env` file for security and ease of use.

## Features

*   **Delete Emails by Sender**: Automatically find and trash all emails from a specific sender.
*   **Delete Emails from a List**: Read a list of email addresses from a file and delete all messages from each of them.
*   **Delete Emails by Age**: Automatically trash all emails older than a specified number of days.
*   **Send Emails**: Send emails with custom HTML content to a specified recipient.
*   **Secure Credential Management**: Uses a `credentials.json` file for Google API access and a `token.pickle` file for storing authorization, both of which are kept private via `.gitignore`.

## Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd GmailCleaner
```

### 2. Install Dependencies

This project uses a few Python libraries. Install them using `pip` and the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 3. Create Your Google Credentials

The script needs access to the Gmail API. To enable this, you must create a `credentials.json` file.

1.  **Go to the Google Cloud Console** and create a new project.
2.  **Enable the Gmail API** for your project.
3.  **Create an OAuth 2.0 Client ID** for a **Desktop app**.
4.  **Download the JSON file** containing your credentials.
5.  **Rename the downloaded file to `credentials.json`** and place it in the root directory of this project.

For a detailed, step-by-step guide, please refer to the instructions provided earlier in our conversation.

### 4. Configure Your Environment

All script settings are managed through a `.env` file. The script will use the credentials from this file to generate the `credentials.json` if it does not exist.

1.  Make a copy of `.env.example` and rename it to `.env` or fill in the existing `.env` file.
2.  Open the `.env` file and fill in the following variables:

```
# --- Main Action ---
# Set the action to perform: "delete-by-sender", "delete-by-age", "send", or ""
ACTION=""

# --- Settings for 'delete-by-sender' ---
SENDER_TO_DELETE="example@example.com"

# --- Settings for 'delete-by-age' ---
DAYS_TO_DELETE=1095  # Default is 3 years

# --- Settings for 'send' ---
RECIPIENT_EMAIL="recipient@example.com"
EMAIL_SUBJECT="Hello from Gemini!"
EMAIL_BODY="<html><body><p>This is a test email.</p></body></html>"

# --- Google Credentials (fill these from your credentials.json file) ---
GOOGLE_CLIENT_ID="YOUR_CLIENT_ID_HERE"
GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE"
GOOGLE_PROJECT_ID="YOUR_PROJECT_ID_HERE"
GOOGLE_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI="https://oauth2.googleapis.com/token"
GOOGLE_AUTH_PROVIDER_URL="https://www.googleapis.com/oauth2/v1/certs"
GOOGLE_REDIRECT_URIS="http://localhost"
```

## Usage

To run the script, first decide what action you want to perform and set the `ACTION` variable in your `.env` file. Then, run `main.py` from your terminal.

1.  **Set the `ACTION` variable** in `.env` to one of the following:
    *   `delete-by-sender`: Deletes emails from the `SENDER_TO_DELETE`.
    *   `delete-from-list`: Deletes emails from every sender listed in `emails_to_delete.txt`.
    *   `delete-by-age`: Deletes emails older than `DAYS_TO_DELETE`.
    *   `send`: Sends an email using the `RECIPIENT_EMAIL`, `EMAIL_SUBJECT`, and `EMAIL_BODY` variables.

2.  **For `delete-from-list`**, add the email addresses you want to target to the `emails_to_delete.txt` file, one per line.

3.  **Run the script**:

    ```bash
    python main.py
    ```

3.  **First-time Authorization**: The first time you run the script, a browser window will open asking you to authorize access to your Gmail account. After you approve, a `token.pickle` file will be created, and the script will not ask for authorization again.

## Security

*   **Never share your `credentials.json`, `.env`, or `token.pickle` files.** These files contain sensitive information.
*   The `.gitignore` file is already configured to exclude these files from being committed to your repository.

## Disclaimer

Please be careful when using the delete functions. Trashing emails is a significant action. It is recommended to first test the script with a specific, non-critical sender or a short time frame to ensure it works as expected.
