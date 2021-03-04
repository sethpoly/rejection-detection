import imaplib
import email
import os
import reject_model
import re
import service_account as acc
from datetime import date
import traceback

# setup rejection detection data model
classifier = reject_model.Classifier()
classifier.clean_data()
classifier.fit()

# Spreadsheet instance
spreadsheet = acc.Spreadsheet('Applications', 'Rejections').sheet


# Add a row to spreadsheet of new application rejection
# @param1: company_name,  @param2: email_body
def add_reject_row(company_name, email_body):
    print('Congrats, another rejection.')
    curr_date = date.today()
    try:
        spreadsheet.append_row([company_name, email_body, curr_date.strftime('%Y/%m/%d')])
    except:
        print('Failed to insert new row.')
        traceback.print_exc()




#add_reject_row('CompanyName', 'email bodagjdgajdgja')

# gmail account credentials
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

                company_name = original['From']
                print(company_name)
                print(original['Subject'])

                # Grab the body of the email
                for part in original.walk():
                    try:
                        if part.get_content_type().lower() == 'text/plain':  # Grab only plaintext
                            body = part.get_payload(decode=True).decode()
                            body = re.sub('<[^<]+?>', '', body)  # Strip HTML tags
                        else:
                            body = part.get_payload(decode=True).decode()
                            body = re.sub('<[^<]+?>', '', body)  # Strip HTML tags
                    except:
                        pass

                print(body)  # Prints the body of the email

                prediction = classifier.predict(body)
                print(prediction)
                if prediction == 'reject':  # move to reject inbox
                    typ, data = imap.store(num, '+X-GM-LABELS', '"Application Updates"')
                    add_reject_row(company_name, body)  # Add entry to spreadsheet

                typ, data = imap.store(num, '-FLAGS', '\\Seen')
                typ, data = imap.store(num, '+X-GM-LABELS',
                                       'Checked')  # Add flag that email was checked whether reject or not
                typ, data = imap.store(num, '+FLAGS', '\\Deleted')  # Delete from inbox

# Close imap connection
close_connection()
