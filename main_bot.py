import os
import requests
import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime

# Fungsi kirim pesan ke Telegram
def kirim_telegram(pesan):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def jalankan_bot():
    print("🚀 Memulai proses Dedik AI...")
    
    # Ambil data dari Secrets GitHub
    creds_json = json.loads(os.getenv('GCP_CREDENTIALS'))
    sheet_id = os.getenv('SPREADSHEET_ID')
    
    # Koneksi ke Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(creds_json, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Data Simulasi Dagang (Bisa Anda ubah nanti)
    nama_barang = "Update Sistem Telegram"
    untung_bersih = 100000 
    waktu = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Tulis ke Google Sheets
    sheet.append_row([waktu, nama_barang, "Otomatis", "Otomatis", untung_bersih])
    
    # Kirim Laporan ke Telegram Anda
    pesan_tele = (
        f"✅ *DEDIK AI: UPDATE BERHASIL*\n\n"
        f"📅 *Waktu:* {waktu}\n"
        f"💰 *Profit:* Rp{untung_bersih:,}\n"
        f"📱 *Status:* Koneksi Sheets & Telegram Aktif!"
    )
    kirim_telegram(pesan_tele)
    print("✅ Selesai! Cek Telegram Anda.")

if __name__ == "__main__":
    jalankan_bot()
