import imaplib
import email
from email.header import decode_header
import webbrowser
import os

# account credentials
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

# create IMAP4 class with SSL
imap = imaplib.IMAP4_SSL('imap.gmail.com')
# authenticate (if fails: <allow less secure apps in gmail account>)
try:
    (retcode, capabilities) = imap.login(username, password)
    print(f'Logged in as {username}.')
except imaplib.IMAP4.error:
    print('Log in failed.')

# Connect to mailbox
imap.select('INBOX')

n = 0
(retcode, messages) = imap.search(None, '(UNSEEN)')  # Filter by unseen messages
if retcode == 'OK':
    for num in messages[0].split():
        print('Processing: ')
        n = n + 1
        typ, data = imap.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                original = email.message_from_bytes(response_part[1])

                print(original['From'])
                print(original['Subject'])

                # Grab the body of the email
                if original.is_multipart():
                    for part in original.walk():
                        try:
                            if part.get_content_type().lower() == 'text/plain':  # Grab only plaintext
                                body = part.get_payload(decode=True).decode()
                        except:
                            pass

                typ, data = imap.store(num, '+FLAGS', '\\Seen')  # Mark msg as seen
                print(body)

try:
    imap.close()
    print('Closed the connection.')
except imaplib.IMAP4.error:
    print('Error: Connection failed to close.')
