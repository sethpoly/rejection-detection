# rejection-detection
A useful machine learning script when sending out hundreds of job applications per week. Filters all rejection emails and organizes them in a live Google Sheets spreadsheet.

## What It Does
- Parses all unread emails every 10 minutes within a Gmail account.
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

## Technology Used
Python, imaplib, pandas, sklearn, Google Drive API