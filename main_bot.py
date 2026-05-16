import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def jalankan_dedik_ai_autopilot_system():
    print("🤖 Memulai Robot DEDIK AI Versi Terbaru...")
    
    # 1. Mengambil Kunci Rahasia dari GitHub Secrets
    token = "8949941557:AAGrK4Wx3FLV0FDpSLlxBCpklidh7Uh6wws"  # Token Baru Langsung Dipasang di Sini
    gcp_json = os.getenv('GCP_CREDENTIALS') or os.getenv('KREDENSIAL GCP')
    sheet_id = os.getenv('SPREADSHEET_ID') or os.getenv('ID_LEMBAR_KELIPATAN')

    if not all([gcp_json, sheet_id]):
        print("❌ Konfigurasi SPREADSHEET_ID atau GCP_CREDENTIALS di GitHub Secrets masih kosong!")
        return

    # 2. SISTEM OTOMATIS MENCARI CHAT ID (ANTI EROR 400)
    print("🔍 Mencari Chat ID kamu secara otomatis ke server Telegram...")
    url_updates = f"https://api.telegram.org/bot{token}/getUpdates"
    chat_id = None
    
    try:
        respon_update = requests.get(url_updates).json()
        if respon_update.get("ok") and respon_update.get("result"):
            # Mengambil ID chat terakhir yang mengirim pesan /start ke bot ini
            for update in reversed(respon_update["result"]):
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    break
    except Exception as e:
        print(f"⚠️ Gagal membaca update otomatis: {e}")

    # Jika pencarian otomatis gagal, gunakan cadangan ID asli kamu kemarin
    if not chat_id:
        print("⚠️ Bot belum mendeteksi pesan masuk. Menggunakan ID cadangan: 8293172022")
        chat_id = "8293172022"
    else:
        print(f"🎯 BERHASIL KETEMU: Mengirim laporan ke Chat ID: {chat_id}")

    waktu_skrg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nama_barang = "Stiker Anti Fog Kaca Spion"
    harga_modal = 5000
    harga_jual = 45928
    untung_bytes = harga_jual - harga_modal

    # ==========================================
    # KONEKSI 1: TEMBAK DATA KE GOOGLE SHEETS
    # ==========================================
    try:
        info_kunci = json.loads(gcp_json)
        if "private_key" in info_kunci and "\\n" not in info_kunci["private_key"]:
            info_kunci["private_key"] = info_kunci["private_key"].replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n").replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")
        
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(info_kunci, scopes=scopes)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(sheet_id).sheet1
        sheet.append_row([waktu_skrg, nama_barang, harga_modal, harga_jual, untung_bytes])
        print("✅ BERHASIL: Data sukses terketik di Google Sheets!")
    except Exception as e:
        print(f"❌ GAGAL MASUK KE GOOGLE SHEETS: {e}")

    # ==========================================
    # KONEKSI 2: TEMBAK LAPORAN KE TELEGRAM
    # ==========================================
    pesan_telegram = (
        f"🚀 *LAPORAN TERBARU DEDIK AI (V3)*\n\n"
        f"📅 *Waktu:* {waktu_skrg}\n"
        f"📦 *Produk:* {nama_barang}\n"
        f"💰 *Harga Modal:* Rp {harga_modal:,}\n"
        f"💸 *Harga Jual:* Rp {harga_jual:,}\n"
        f"📈 *Profit Bersih:* Rp {untung_bytes:,}\n\n"
        f"Sistem Baru Sukses Menulis ke Sheets! 🦾"
    )
    
    url_telegram = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": str(chat_id),
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
