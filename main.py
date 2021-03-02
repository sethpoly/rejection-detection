import imaplib
import email
import os
import reject_model
import re

# setup rejection detection data model
classifier = reject_model.Classifier()
classifier.clean_data()
classifier.fit()

# account credentials
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

# create IMAP4 class with SSL
imap = imaplib.IMAP4_SSL('imap.gmail.com')


# authenticate (if fails: <allow less secure apps in gmail account>)
def authenticate():
    try:
        (retcode, capabilities) = imap.login(username, password)
        print(f'Logged in as {username}.')
    except imaplib.IMAP4.error:
        print('Log in failed.')


# Close the imap connection
def close_connection():
    try:
        imap.close()
        print('Closed the connection.')
    except imaplib.IMAP4.error:
        print('Error: Connection failed to close.')


# Login credentials with mail client
authenticate()

# Connect to mailbox
imap.select('INBOX')
(retcode, messages) = imap.search(None, '(UNSEEN)')  # Filter by unseen messages
n = 0
if retcode == 'OK':
    for num in messages[0].split():  # Loop each unread email
        print('Processing: ')
        n = n + 1
        body = ''
        typ, data = imap.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                original = email.message_from_bytes(response_part[1])

                print(original['From'])
                print(original['Subject'])

                # Grab the body of the email
                # if original.is_multipart():
                for part in original.walk():
                    try:
                        if part.get_content_type().lower() == 'text/plain':  # Grab only plaintext
                            body = part.get_payload(decode=True).decode()
                        elif part.get_content_type().lower() == 'text/html':  # strip html
                            body = part.get_payload(decode=True).decode()
                            body = re.sub('<[^<]+?>', '', body)
                    except:
                        pass

                print(body)  # Prints the body of the email

                prediction = classifier.predict(body)
                print(prediction)
                if prediction == 'reject':  # move to reject inbox
                    typ, data = imap.store(num, '+X-GM-LABELS', '"Application Updates"')

                typ, data = imap.store(num, '-FLAGS', '\\Seen')
                typ, data = imap.store(num, '+X-GM-LABELS',
                                       'Checked')  # Add flag that email was checked whether reject or not
                typ, data = imap.store(num, '+FLAGS', '\\Deleted')  # Delete from inbox

# Close imap connection
close_connection()