import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

if not SPREADSHEET_ID or not SERVICE_ACCOUNT_FILE:
    raise ValueError("⚠️ Verifique se SPREADSHEET_ID e SERVICE_ACCOUNT_FILE estão definidos no .env.")

# Autenticação
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(creds)

def get_sheets_data():
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    data = sheet.get_all_records()
    return data
