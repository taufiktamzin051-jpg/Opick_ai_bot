import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def jalankan_dedik_ai_autopilot_system():
    print("🤖 Memulai Robot DEDIK AI Versi 3.9 (Sistem Kunci JSON Baru Otomatis)...")
    
    token = "8949941557:AAGrK4Wx3FLV0FDpSLlxBCpklidh7Uh6wws"
    gcp_json_raw = os.getenv('GCP_CREDENTIALS')
    sheet_id = os.getenv('SPREADSHEET_ID') or os.getenv('ID_LEMBAR_KELIPATAN')

    if not gcp_json_raw or not sheet_id:
        print("❌ ERROR: GCP_CREDENTIALS atau SPREADSHEET_ID di GitHub Secrets masih kosong!")
        return

    # 1. AMBIL CHAT ID TELEGRAM OTOMATIS
    url_updates = f"https://api.telegram.org/bot{token}/getUpdates"
    chat_id = None
    try:
        respon_update = requests.get(url_updates).json()
        if respon_update.get("ok") and respon_update.get("result"):
            for update in reversed(respon_update["result"]):
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    break
    except:
        pass

    if not chat_id:
        chat_id = "8293172022"

    waktu_skrg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nama_barang = "Stiker Anti Fog Kaca Spion"
    harga_modal = 5000
    harga_jual = 45928
    untung_bytes = harga_jual - harga_modal

    # ==========================================
    # KONEKSI 1: GOOGLE SHEETS VIA RAW JSON DARI GITHUB SECRETS
    # ==========================================
    try:
        json_clean = gcp_json_raw.strip()
        info_kunci = json.loads(json_clean)
        
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
        f"🚀 *LAPORAN TERBARU DEDIK AI (V3.9)*\n\n"
        f"📅 *Waktu:* {waktu_skrg}\n"
        f"📦 *Produk:* {nama_barang}\n"
        f"💰 *Harga Modal:* Rp {harga_modal:,}\n"
        f"💸 *Harga Jual:* Rp {harga_jual:,}\n"
        f"📈 *Profit Bersih:* Rp {untung_bytes:,}\n\n"
        f"Sistem Autopilot Google Sheets & Telegram Berjalan Sempurna! 🦾"
    )
    
    url_telegram = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": str(chat_id), "text": pesan_telegram, "parse_mode": "Markdown"}
    
    try:
        respon = requests.post(url_telegram, json=payload)
        if respon.status_code == 200:
            print("🚀 BERHASIL: Laporan profit asli terkirim ke Telegram!")
        else:
            print(f"❌ GAGAL KE TELEGRAM: Kode Status {respon.status_code}")
    except Exception as e:
        print(f"❌ GAGAL MENGHUBUNGI SERVER TELEGRAM: {e}")

if __name__ == "__main__":
    jalankan_dedik_ai_autopilot_system()
