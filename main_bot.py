import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

def lapor_otomatis_final():
    # 1. Ambil data dari GitHub Secrets
    token = os.getenv('TOKEN_TELEGRAM')
    chat_id = os.getenv('ID_CHAT_TELEGRAM')
    gcp_json = os.getenv('KREDENSIAL_GCP')
    sheet_id = os.getenv('ID_LEMBAR_KELIPATAN')

    try:
        # 2. Akses Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(gcp_json), scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Ambil data terbaru (baris paling bawah)
        records = sheet.get_all_records()
        
        if records:
            data_terakhir = records[-1]
            waktu_skrg = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Susun template pesan laporan
            pesan = f"🤖 **LAPORAN TRANSAKSI DEDIK AI**\n"
            pesan += f"⏰ Waktu Cek: {waktu_skrg} WIB\n"
            pesan += f"━━━━━━━━━━━━━━━\n"
            for k, v in data_terakhir.items():
                if k: # Hanya masukkan jika judul kolom tidak kosong
                    pesan += f"📍 **{k}**: {v}\n"
            pesan += f"━━━━━━━━━━━━━━━\n"
            pesan += f"✅ Data berhasil diamankan, Bos! 🔥"
        else:
            pesan = "⚠️ Bot berjalan aktif, tapi data di Google Sheets masih kosong, Bro."

        # 3. Kirim langsung ke Telegram
        url_tele = f"https://api.telegram.org/bot{token}/sendMessage"
        payload_tele = {"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"}
        
        respons = requests.post(url_tele, json=payload_tele)
        
        if respons.status_code == 200:
            print("✅ Laporan sukses terkirim ke Telegram!")
        else:
            print(f"❌ Telegram menolak dengan kode: {respons.status_code}")

    except Exception as e:
        print(f"❌ Error sistem: {e}")

if __name__ == "__main__":
    lapor_otomatis_final()
