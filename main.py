import imaplib
import email
import os
import reject_model
import re
import service_account as acc
from datetime import date
import traceback
from bs4 import BeautifulSoup
import time
import gspread

# setup rejection detection data model
classifier = reject_model.Classifier()
classifier.clean_data()
classifier.fit()


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


# Clean email output of all script tags/html/css etc
def clean_text(text):
    text = re.sub(r'\. \{.*\}', '', text)  # Strip CSS
    text = remove_whitespace(text)  # Remove invisible carriage returns etc

    soup = BeautifulSoup(text, 'html.parser')
    for s in soup(['script', 'style']):
        s.extract()
    return ' '.join(soup.stripped_strings)


# Remove all white space and carriage returns
def remove_whitespace(text):
    chars = ['\n', '\t', '\r']
    for ch in chars:
        if ch in text:
            text = text.replace(ch, '')
    return text


# gmail account credentials
username = os.environ['GMAIL']
password = os.environ['GMAIL_PASS']

# create IMAP4 class with SSL
imap = imaplib.IMAP4_SSL('imap.gmail.com')


# authenticate (if fails: <allow less secure apps in gmail account>)
def authenticate():
    try:
        (retcode, capabilities) = imap.login(username, password)
        print(f'Logged in as {username}.')
    except imaplib.IMAP4.error:
        traceback.print_exc()


# Close the imap connection
def close_connection():
    try:
        imap.close()
        imap.logout()
        print('Closed the connection.')
    except imaplib.IMAP4.error:
        print('Error: Connection failed to close.')


# authenticate()  # Login with imap


def check_mailbox():
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
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                    body = clean_text(body)  # Clean formatting of email
                    print(body)

                    # Predict if the email is a rejection email
                    prediction = classifier.predict(body)
                    print(prediction)
                    if prediction == 'reject':  # move to reject inbox
                        typ, data = imap.store(num, '+X-GM-LABELS', '"Application Updates"')
                        add_reject_row(company_name, body)  # Add entry to spreadsheet

                    # Remove SEEN flag
                    typ, data = imap.store(num, '-FLAGS', '\\Seen')
                    # Move to CHECKED inbox
                    typ, data = imap.store(num, '+X-GM-LABELS',
                                           'Checked')
                    # Delete from inbox
                    typ, data = imap.store(num, '+FLAGS', '\\Deleted')

    close_connection()


# Main loop, every ten minutes check email for rejections
while True:
    try:
        spreadsheet = acc.Spreadsheet('Applications', 'Rejections').sheet  # open spreadsheet instance
        imap = imaplib.IMAP4_SSL('imap.gmail.com')  # recreate IMAP4 class with SSL to avoid timeout
        authenticate()  # login to gamil through imap
        check_mailbox()  # check email
        print('Waiting 10 minutes to check email again...')
        time.sleep(600)
    except KeyboardInterrupt:
        print('Interrupted... Ending application')
        exit()
    except gspread.exceptions.APIError:
        print('Something went wrong, lets try this again.')
        pass
