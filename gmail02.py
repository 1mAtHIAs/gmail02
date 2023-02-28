from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def get_messages(service):
    results = service.users().messages().list(userId='me').execute()
    msg_ids = []
    num = int(input('Hányat szeretnél megjeleníteni a legutóbb beérkezett e-mailjeid közül? '))
    fromwho = input('Szeretnéd látni kitől érkeztek az e-mailek?(igen/nem) ')
    subj = input('Szeretnéd látni az érkezett e-mailek tárgyát?(igen/nem) ')
    when = input('Szeretnéd látni mikor érkeztek az e-mailek?(igen/nem) ')
    print('')
    for msg in results['messages']:
        msg_ids.append(msg['id'])
    for index in range(num):
        message = service.users().messages().get(userId='me',
                                                 id=msg_ids[index], format='metadata').execute()
        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == 'From' and fromwho == 'igen':
                print(f'From: {header["value"]}')
            elif header['name'] == 'Subject' and subj == 'igen':
                print(f'Subject: {header["value"]}')
            elif header['name'] == 'Date' and when == 'igen':
                print(f'\nDate: {header["value"]}')


def main():
    service = get_service()
    get_messages(service)


main()
