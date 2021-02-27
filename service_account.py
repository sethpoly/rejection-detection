import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class Spreadsheet:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # define the scope
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google_key.json', scope)  # account credentials
    client = gspread.authorize(credentials)  # authorize clientsheet

    sheet = None  # Specific sheet in CSV file

    # Grab the name of spreadsheet on init
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.open_sheet()

    # Open spreadsheet for editing and parsing
    def open_sheet(self):
        try:
            self.sheet = self.client.open(self.sheet_name).sheet1
            print(f'Opened sheet: {self.sheet_name}')
        except gspread.SpreadsheetNotFound:
            print('Spreadsheet does not exist.')

# app_sheet = Spreadsheet('Applications').sheet
#
# print(app_sheet.acell('A400').value)
