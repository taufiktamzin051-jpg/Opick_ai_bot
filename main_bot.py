import gspread
from google.oauth2.service_account import Credentials
import os
import json
import requests
from datetime import datetime

# --- 1. SETUP KREDENSI ---
# Mengambil kunci rahasia dari GitHub Secrets yang Anda buat
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds_dict = json.loads(os.getenv('GCP_CREDENTIALS'))
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# --- 2. FUNGSI AUTO-SETUP GOOGLE SHEETS ---
def setup_opick_ai():
    nama_file = "Opick_AI_Master"
    try:
        # Mencoba membuka file jika sudah ada
        sheet = client.open(nama_file).sheet1
        print("✅ File Sheets sudah siap.")
    except:
        # Jika belum ada, Opick AI akan membuatnya otomatis
        print("📂 Membuat file Sheets baru untuk Opick AI...")
        new_sheet = client.create(nama_file)
        sheet = new_sheet.sheet1
        header = ["Nama Produk", "Harga Supplier", "Harga Kompetitor", "Harga Jual", "Status", "Profit"]
        sheet.insert_row(header, 1)
        print(f"🚀 File {nama_file} berhasil dibuat!")
    return sheet

# --- 3. LOGIKA ROBOT HUNTER (SIMULASI PERBURUAN) ---
def robot_hunter():
    # Simulasi pencarian barang murah (Bisa dikembangkan sesuai supplier Anda)
    temuan = [
        {"nama": "Kabel Data Fast Charging", "harga_s": 8000, "harga_k": 15000},
        {"nama": "Stand HP Lipat", "harga_s": 12000, "harga_k": 25000}
    ]
    return temuan

# --- 4. FUNGSI LAPORAN TELEGRAM ---
def kirim_laporan(pesan):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# --- 5. EKSEKUSI UTAMA ---
if __name__ == "__main__":
    try:
        # Inisialisasi Sheets
        sheet = setup_opick_ai()
        
        # Mulai berburu
        barang_baru = robot_hunter()
        
        # Kirim notifikasi ke Telegram
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M")
        pesan_tele = (
            f"🤖 *LAPORAN OPICK AI*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📅 *Waktu:* `{waktu}`\n"
            f"🔎 *Status:* Berhasil Sinkronisasi Sheets\n"
            f"📦 *Temuan:* Berhasil memantau {len(barang_baru)} produk baru.\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ *Sistem:* Running Smooth"
        )
        kirim_laporan(pesan_tele)
        print("🚀 Selesai! Cek Telegram dan Google Sheets Anda.")
        
    except Exception as e:
        error_msg = f"❌ *Opick AI Error:* {str(e)}"
        kirim_laporan(error_msg)
        print(f"Terjadi kesalahan: {e}")
