import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re


class Spreadsheet:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # define the scope
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google_key.json', scope)  # account credentials
    client = gspread.authorize(credentials)  # authorize clientsheet

    sheet = None  # Specific sheet in CSV file

    # Grab the name of spreadsheet on init
    def __init__(self, sheet_name, sheet_page):
        self.sheet_name = sheet_name
        self.open_sheet(sheet_page)

    # Open spreadsheet for editing and parsing
    def open_sheet(self, sheet_page):
        try:
            self.sheet = self.client.open(self.sheet_name).worksheet(sheet_page)
            print(f'Opened sheet: {self.sheet_name}')
        except gspread.SpreadsheetNotFound:
            print('Spreadsheet does not exist.')


# Populate empty cells with boolean values
# Useful when building data-dashboard
def organize_data():
    sheet = Spreadsheet('Applications', 'Main').sheet  # Open sheet
    cell_list = sheet.range('I2:I566')

    for cell in range(len(cell_list)):
        if cell_list[cell].value == 'coverletter':
            cell_list[cell].value = 'True'

    sheet.update_cells(cell_list)



