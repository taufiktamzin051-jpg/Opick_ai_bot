import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

def lapor_otomatis():
    # Ambil data dari Secrets
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    gcp_json = os.getenv('KREDENSIAL_GCP')
    sheet_id = os.getenv('ID_LEMBAR_KELIPATAN')

    try:
        # Akses Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(gcp_json), scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Ambil data terbaru (baris paling bawah)
        records = sheet.get_all_records()
        
        if records:
            data_terakhir = records[-1]
            waktu_skrg = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            pesan = f"🤖 **LAPORAN OTOMATIS DEDIK AI**\n"
            pesan += f"⏰ Waktu: {waktu_skrg} WIB\n"
            pesan += f"━━━━━━━━━━━━━━━\n"
            for k, v in data_terakhir.items():
                pesan += f"📍 **{k}**: {v}\n"
        else:
            pesan = "⚠️ Bot berjalan, tapi data di Spreadsheet kosong."

        # Kirim ke Telegram
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"})
        
        print("✅ Laporan otomatis terkirim!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    lapor_otomatis()
