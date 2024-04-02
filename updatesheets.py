import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials

# Replace 'YOUR_SPREADSHEET_ID' with the actual Google Sheets document ID
spreadsheet_chronological = '136eifqbDBkAym0A6ejxeM6N7FLJShTIiPVflOhfQLFw'
spreadsheet_cores = '1jH1QgfxM1Hsqi9VbBLioDS18EdagVX2dfyLmxGnOO7Y'

# Replace 'YOUR_SHEET_NAME' with the name of the sheet you want to download
sheet_name1 = 'ChronoligcalOrder'
sheet_name2 = 'Block 5'

# Path to your Google Sheets API credentials JSON file
credentials_file = 'credentials.json'

# Authenticate with the Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)

# Open the Google Sheets document by ID
spreadsheet_chron = client.open_by_key(spreadsheet_chronological)
spreadsheet_cores = client.open_by_key(spreadsheet_cores)

# Get the specific sheet by name
sheet = spreadsheet_chron.worksheet(sheet_name1)
sheet2 = spreadsheet_cores.worksheet(sheet_name2)

# Get all values from the sheet
data = sheet.get_all_values()
data2 = sheet2.get_all_values()


with open("ChronologicalOrder.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

with open("FalconCores.csv", "w") as csv_file:
      writer = csv.writer(csv_file, delimiter=',')
      for line in data2:
            writer.writerow(line)