# rejection-detection
A useful machine learning script when sending out hundreds of job applications per week. Filters all rejection emails and organizes them in a live Google Sheets spreadsheet.

## What It Does
- Parses all unread emails every 30 minutes within a Gmail account.
- Determines if each email is a rejection or non_rejection using the machine learning classifier.
- If a rejection email is found: 
    - move email to the "Rejection" inbox
    - update the rejection spreadsheet using the company name, email body, and date rejected
- If non_rejection email is found:
    - move email to the "Checked" inbox
    - continue checking emails


## Machine Learning
- View notebook at https://www.kaggle.com/sethpoly/detect-reject-emails
- View dataset at https://www.kaggle.com/sethpoly/application-rejection-emails
- Developed a model to classify emails as either "rejection" or "non-rejection"
- Implemented Naive Bayes classifier

## Visual Example
Filters unread emails every 30 minutes, and categorizes them as rejection/non_rejection:

![Preview](https://raw.githubusercontent.com/sethpoly/rejection-detection/master/screenshots/terminal.PNG) 

\
If rejection email is found, connect to Google Sheets API and create an entry in the spreadsheet containing the company that rejected me.

![Preview](https://raw.githubusercontent.com/sethpoly/rejection-detection/master/screenshots/sheet.PNG)

## Technology Used
Python, imaplib, pandas, sklearn, Google Drive API

