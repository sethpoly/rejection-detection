import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class Spreadsheet:
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # account credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google_key.json', scope)

    # authorize clientsheet
    client = gspread.authorize(credentials)

    # Grab the name of spreadsheet on init
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.open_sheet()

    # Open spreadsheet for editing and parsing
    def open_sheet(self):
        try:
            self.sheet = self.client.open(self.sheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            print('Spreadsheet does not exist.')


# app_sheet = Spreadsheet('Applications').sheet
#
# print(app_sheet.acell('A400').value)
