# rejection-detection
A useful script when sending out 100's of job applications per week. Filters all rejection emails and organizes them in a Google Sheets spreadsheet.

## What It Does
- Watches any Gmail account, and filters all unread rejection emails from job applications.
- Parses the rejection email and adds an entry to a Google Sheet for organization.

## Machine Learning
- View notebook at https://www.kaggle.com/sethpoly/detect-reject-emails
- Developed a model to classify emails as either "rejection" or "non-rejection"
- Implemented Naive Bayes classifier


## Technology Used
Python, imaplib, pandas, numpy, sklearn, matplotlib, Google Drive API