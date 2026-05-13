import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def jalankan_bot():
    print("🚀 Memulai Bot Dedik AI...")

    # 1. Mengambil Kredensial dari GitHub Secrets
    creds_json = os.environ.get('GCP_CREDENTIALS')
    sheet_id = os.environ.get('SPREADSHEET_ID')

    if not creds_json or not sheet_id:
        print("❌ Error: Kredensial atau Spreadsheet ID tidak ditemukan di Secrets!")
        return

    try:
        # 2. Setup Koneksi ke Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # 3. Buka Spreadsheet (Berdasarkan ID agar tidak kena error Quota Drive)
        sheet = client.open_by_key(sheet_id).sheet1
        
        # 4. Contoh Input Data (Anda bisa sesuaikan bagian ini)
        data_baru = ["Dedik AI", "Status: Aktif", "Berhasil Update"]
        sheet.append_row(data_baru)
        
        print("✅ Berhasil! Data sudah masuk ke Google Sheets.")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    jalankan_bot()

