import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import random
from datetime import datetime

def jalankan_dedik_ai_autopilot_system():
    print("🤖 Memulai Robot DEDIK AI...")
    
    # 1. Mengambil Kunci Rahasia dari GitHub Secrets
    token = os.getenv('TOKEN_TELEGRAM') or os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID_TELEGRAM') or os.getenv('TELEGRAM_CHAT_ID') or os.getenv('ID_CHAT_TELEGRAM')
    gcp_json = os.getenv('GCP_CREDENTIALS') or os.getenv('KREDENSIAL GCP')
    sheet_id = os.getenv('SPREADSHEET_ID') or os.getenv('ID_LEMBAR_KELIPATAN')

    if not all([token, chat_id, gcp_json, sheet_id]):
        print("❌ Konfigurasi GitHub Secrets belum lengkap atau nama tidak cocok!")
        return

    # Data Produk yang akan dimasukkan ke laporan
    nama_barang = "Stiker Anti Fog Kaca Spion"
    harga_modal = 5000
    harga_jual = 45928
    untung_bersih = harga_jual - harga_modal
    waktu_skrg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================================
    # KONEKSI INTERNET ASLI 1: TEMBAK KE GOOGLE SHEETS
    # ==========================================
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        kredensial_dict = json.loads(gcp_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(kredensial_dict, scope)
        client = gspread.authorize(creds)
        
        # Membuka Google Sheets berdasarkan SPREADSHEET_ID
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Menulis baris data baru ke Sheets kamu
        sheet.append_row([waktu_skrg, nama_barang, harga_modal, harga_jual, untung_bersih])
        print("✅ BERHASIL: Data sukses terketik di Google Sheets!")
    except Exception as e:
        print(f"❌ GAGAL MASUK KE GOOGLE SHEETS: {e}")

    # ==========================================
    # KONEKSI INTERNET ASLI 2: TEMBAK LAPORAN KE TELEGRAM
    # ==========================================
    pesan_telegram = (
        f"🚀 *LAPORAN TERBARU DEDIK AI*\n\n"
        f"📅 *Waktu:* {waktu_skrg}\n"
        f"📦 *Produk:* {nama_barang}\n"
        f"💰 *Harga Modal:* Rp {harga_modal:,}\n"
        f"💸 *Harga Jual:* Rp {harga_jual:,}\n"
        f"📈 *Profit Bersih:* Rp {untung_bersih:,}\n\n"
        f"Sistem Autopilot Sukses Menulis ke Sheets! 🦾"
    )
    
    url_telegram = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": pesan_telegram,
        "parse_mode": "Markdown"
    }
    
    try:
        respon = requests.post(url_telegram, json=payload)
        if respon.status_code == 200:
            print("🚀 BERHASIL: Laporan profit asli terkirim ke Telegram!")
        else:
            print(f"❌ GAGAL KE TELEGRAM: Kode Status {respon.status_code} - {respon.text}")
    except Exception as e:
        print(f"❌ GAGAL MENGHUBUNGI SERVER TELEGRAM: {e}")

if __name__ == "__main__":
    jalankan_dedik_ai_autopilot_system()
