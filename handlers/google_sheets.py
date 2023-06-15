import asyncio

import gspread
from decouple import config
from oauth2client.service_account import ServiceAccountCredentials

sheet_url = config("SHEET_URL")
credentials_path = "heg-champ-2023-0e6125675701.json"
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


async def reading_all_data(name, nomination):
    column_c_values = worksheet.col_values(3)
    column_e_values = worksheet.col_values(5)
    target_name = name
    target_value = nomination
    matching_rows = [
        row_index + 1
        for row_index, (name, value) in enumerate(zip(column_c_values, column_e_values))
        if name.strip() == target_name and value.strip() == target_value
    ]
    all_values = []
    for row_index in matching_rows:
        row_values = worksheet.row_values(row_index)
        all_values.append(row_values)
    return all_values

asyncio.run(reading_all_data("Тестовый Аккаунт", "Ровный срез"))
