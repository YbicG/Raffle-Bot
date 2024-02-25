from googleapiclient.discovery import build
from google.oauth2 import service_account
import database

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file('Discord Bots/Raffle Bot/Database/credentials.json', scopes=SCOPES)

spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

class RangeNames():
    discord_id = "A"
    roblox_username = "B"
    balance = "C"
    discord_username = "D"

def update_google_sheet(file_type, key, value):
    if file_type == database.FileType.balance:
        spreadsheet_id = '16uy4rFJ2Pa2bncUGDOva-zqfzPsH1vOdj4xU3Q7ehgU'
        range_name = 'Sheet1!A2'
    elif file_type == database.FileType.roblox_accounts:
        spreadsheet_id = '1fpecNNkm5RHvcmU3iCWspDJ7z6xZokBLL0_gXLnnIAc'
        range_name = 'Sheet1!A2'
    else:
        return

    values = [
        [value["roblox_username"], value["balance"], value["discord_username"]]
    ]
    
    body = {
        'values': values
    }
    result = spreadsheet_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body
    ).execute()
    print('Cell updated:', result)

