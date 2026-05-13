import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def jalankan_bot():
    print("🚀 Mencoba membuka file yang sudah ada...")
    creds_json = os.environ.get('GCP_CREDENTIALS')
    sheet_id = os.environ.get('SPREADSHEET_ID')

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # INI KUNCI PERBAIKANNYA: Menggunakan open_by_key, bukan create
        sheet = client.open_by_key(sheet_id).sheet1
        
        sheet.append_row(["Dedik AI", "Update", "Berhasil"])
        print("✅ Data BERHASIL masuk ke Sheets Anda!")

    except Exception as e:
        print(f"❌ Masalah: {str(e)}")

if __name__ == "__main__":
    jalankan_bot()


