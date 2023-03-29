import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Replace with your actual OAuth 2.0 client secrets file path
CLIENT_SECRETS_FILE = 'path/to/client_secret.json'

# Define the scopes that you want to use
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Create the authorization flow instance
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

# Run the authorization flow
creds = None
if not creds or not creds.valid:
    creds = flow.run_local_server(port=0)

# Build the Gmail API service
service = build('gmail', 'v1', credentials=creds)

# Construct the message
message = MIMEText('Hello, World!')
message['to'] = 'recipient@example.com'
message['subject'] = 'Test Email'

# Encode the message in base64url format
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

# Send the message using the Gmail API
try:
    message = service.users().messages().send(
        userId='me',
        body={'raw': raw_message}).execute()
    print('Message Id: %s' % message['id'])
except HttpError as error:
    print('An error occurred: %s' % error)
