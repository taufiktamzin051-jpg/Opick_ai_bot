import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def jalankan_dedik_ai_autopilot_system():
    print("🤖 Memulai Robot DEDIK AI Versi 3.8 (Sistem Kunci Hardcoded Multi-line)...")
    
    token = "8949941557:AAGrK4Wx3FLV0FDpSLlxBCpklidh7Uh6wws"
    sheet_id = os.getenv('SPREADSHEET_ID') or os.getenv('ID_LEMBAR_KELIPATAN')

    if not sheet_id:
        print("❌ Konfigurasi SPREADSHEET_ID di GitHub Secrets masih kosong!")
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
    # KONEKSI 1: GOOGLE SHEETS VIA MULTI-LINE STRING
    # ==========================================
    try:
        # Menyusun kunci rahasia secara berbaris agar aman dari error pemotongan teks HP
        kunci_privat_gcp = (
            "-----BEGIN PRIVATE KEY-----\n"
            "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+65vUL236W2ag\n"
            "DMkoBdju1LP58jjcF0kykpilz6FPCmv6H+VdOXlsw9+21cP/7iSn2O3Ma7yi92At\n"
            "UMfHlM06baA954wlgpEqREaLxCS5vp2y4Lr+m5CrUP7vwgHeYQ6cSHZo1YhuhCa\n"
            "6GxBwF847fvvBeKnWJCvc+JuuyXbV48HEiq59NFw+PAZn8yjzruSACtAY1L21gRm\n"
            "BcqKEfCJboa9aPcpHlGwcQ36ZcwIU9++RDQSjJvfmTgNs7ySDBRcUTvLXGgDkPcf\n"
            "1wDvfY69TN53zdN72IWCXJhCobk59zTmeoa9qLw4HoFW0Tacxsgvy/JBXk6U1HhZ\n"
            "lsA9WrtjAgMBAAECggEAEqqHdEHk30bjbD+DxUl5EbSzGftgKsiODAdALGn16/vp\n"
            "Xa2Tp78wS32FGGOjA5k9dTmk2kkoSsij2IBnXRoCaZh2EvriuP5aZ6cd+HDkjnBN\n"
            "yaKRHNBBynwVOv5M4yoyzuHzvMsW5zpBWFvkBbOwu6is6owpQlJK5xSN7WSXyW+F\n"
            "WKO6YHeZtfpwnHwH1uHcolvgFJndnOCYfJRdlf57H32hbkugHUkgxf2TsxYKsO7k\n"
            "B90JA1AmpkAy5A31Dic29gCFm9D3+sYmsR5jPRObWsBMdnPuViMzLwTiYZYvFHBr\n"
            "mQGPt6SNmGcDTKRW4AEZ054nmB/1bMwg7Hvlv9kEpQKBgQDkD8yBBq7hTKceISC1\n"
            "pxt/ACHdmTpj7l7x8y4uu4cKS357tVZ4OdeSVtP4tFiPZDvilccZcjnq2jL0GBK3\n"
            "242/3byrMn5KtOkvlNukpmNio2FAh4fWqXm/AR0BnCKjxzs+5+xOMi5+0I/od6Ws\n"
            "vxK9xHjit4uQX0OGly5LUsFCVQKBgQDWTwa8aRnc0kUNNEz5vq9M8RitZtZhxNYG\n"
            "ntyDL1g0VBztMTEpBDP3pE4/Kg8UM5d+TklyqvlJA5Xuif6Ih+WJg1NHolJwKQoY9\n"
            "eVHD013LuEnl3T1tEUZpPtLR5vA0XfVkY0+lMHkr7UGKFTIFXflThlqA5PRNOzzG\n"
            "L5tylt3u1wKBgQCiC2+9hegggXyE9fjt2Wy6Enf9onBQrQCdXbLE1c4fzIB0meZ0\n"
            "ynSXsEYxAsOiLxA18UJknDr22k82DRzPsprHZ2A1LE17+4tsmZJvLSKU5Y2mciZ\n"
            "YcqlKtGrdne29Je7hm/Bd1gEZ1KO/3t3vqgGFqoP1b6hqqXGX4bdchAg37eQKBgQCV\n"
            "p0fX6Dj0OC2aI+yg9iSqQS5vYIHSckbXF6iiTw6BobQp+phbxrvEuDFQRSYkdJ3l\n"
            "Cm8FmLQNt3LXrfNFcEXfwp32oVg53eyqHv8XFZHJQh7wksdjU43szr8fbvpMR1S\n"
            "mTqd+flQPdbWvvFP3DgOe7RJkMf3btMMiznnp0iqWrwKBgFoPCPNnznMPO/fDWAT\n"
            "F6BCseeptEMOVJX0qsLRUNrdFXOUj5L83TPxwarEkKPLzaidLzWm3bmhu6lnnSAS\n"
            "hTd+vUZto+atwI/UzZBftpYhMajv+5i/+67tP14dnRjC5sdC0hNOZB9SjkD4cDcB\n"
            "G0tyMSBGPs0ycLGFBELd0UZmC\n"
            "-----END PRIVATE KEY-----\n"
        )
        
        # Integrasi komponen konfigurasi pelengkap secara internal
        gcp_config = {
            "type": "service_account",
            "project_id": "winged-scout-467517-c5",
            "private_key_id": "a9d3c4a27c99bd6597b347a281d23791d866bcf5",
            "private_key": kunci_privat_gcp,
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
        f"🚀 *LAPORAN TERBARU DEDIK AI (V3.8)*\n\n"
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
