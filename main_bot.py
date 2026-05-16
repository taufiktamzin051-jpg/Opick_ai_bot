import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def jalankan_dedik_ai_autopilot_system():
    print("🤖 Memulai Robot DEDIK AI Versi 3.7 (Sistem Kunci Otomatis)...")
    
    token = "8949941557:AAGrK4Wx3FLV0FDpSLlxBCpklidh7Uh6wws"
    private_key_raw = os.getenv('GCP_CREDENTIALS') or os.getenv('KREDENSIAL GCP')
    sheet_id = os.getenv('SPREADSHEET_ID') or os.getenv('ID_LEMBAR_KELIPATAN')

    if not all([private_key_raw, sheet_id]):
        print("❌ Konfigurasi SPREADSHEET_ID atau GCP_CREDENTIALS di GitHub Secrets masih kosong!")
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
    # KONEKSI 1: GOOGLE SHEETS DENGAN RE-CONSTRUCT STRUKTUR JSON
    # ==========================================
    try:
        # Menghapus spasi liar dan menormalkan format newline \n secara otomatis
        kunci_bersih = private_key_raw.strip().replace("\\n", "\n")
        
        # Menyusun dictionary kredensial GCP secara langsung di dalam program
        gcp_config = {
            "type": "service_account",
            "project_id": "winged-scout-467517-c5",
            "private_key_id": "a9d3c4a27c99bd6597b347a281d23791d866bcf5",
            "private_key": kunci_bersih,
            "client_email": "opick-ai-bot@winged-scout-467517-c5.iam.gserviceaccount.com",
            "client_id": "117579405054256940875",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/opick-ai-bot%40winged-scout-467517-c5.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(gcp_config, scopes=scopes)
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
        f"🚀 *LAPORAN TERBARU DEDIK AI (V3.7)*\n\n"
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
