import gspread
from decouple import config
from oauth2client.service_account import ServiceAccountCredentials

sheet_url = config("SHEET_URL")
credentials_path = "json/heg-champ-2023-0e6125675701.json"
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url(sheet_url)
worksheet = sh.get_worksheet(0)


async def write_answers_to_sheet(data, work, category):
    row = [int(data.get('work')), (data.get('referee')), work[1], category, work[2], int(data.get('grades1')),
           int(data.get('grades2')),
           int(data.get('grades3')), int(data.get('grades4')), int(data.get('grades5')), int(data.get('grades6')),
           int(data.get('grades7')), int(data.get('grades8')), int(data.get('grades9')),
           int(data.get('grades10')), int(data.get('grades11')), int(data.get('grades12')),
           int(data.get('grades13')), int(data.get('grades14')), int(data.get('grades15')),
           int(data.get('grades16')), int(data.get('grades17')), int(data.get('penalty')), data.get('advice')]
    worksheet.append_row(row, 2)
