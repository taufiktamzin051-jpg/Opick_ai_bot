import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

def lapor_otomatis_v2():
    # 1. Ambil data dari GitHub Secrets
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    gcp_json = os.getenv('KREDENSIAL_GCP')
    sheet_id = os.getenv('ID_LEMBAR_KELIPATAN')
    gemini_key = os.getenv('GEMINI_API_KEY')  # Pastikan API Key Gemini ada di Secrets

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
            
            # Format pesan dasar data dari Google Sheets
            isi_data = ""
            for k, v in data_terakhir.items():
                isi_data += f"📍 **{k}**: {v}\n"
            
            # 3. Otak AI Baru (Gemini 1.5 Flash) untuk bikin kata-kata laporan otomatis
            analisis_ai = "Sukses mencatat transaksi terbaru!"
            if gemini_key:
                try:
                    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                    payload = {
                        "contents": [{
                            "parts": [{
                                "text": f"Kamu adalah asisten toko online bernama DEDIK AI. Berikan satu kalimat singkat, padat, bersemangat, atau analisis singkat tentang penjualan ini untuk Bos Dedik: {isi_data}"
                            }]
                        }]
                    }
                    respons = requests.post(url_gemini, json=payload)
                    if respons.status_code == 200:
                        analisis_ai = respons.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                except Exception:
                    analisis_ai = "Sukses mengamankan pesanan baru, Bos! 🔥"

            # 4. Susun Pesan Final Telegram
            pesan = f"🤖 **LAPORAN OTOMATIS DEDIK AI v2**\n"
            pesan += f"⏰ Waktu Pengecekan: {waktu_skrg} WIB\n"
            pesan += f"━━━━━━━━━━━━━━━\n"
            pesan += isi_data
            pesan += f"━━━━━━━━━━━━━━━\n"
            pesan += f"💡 **Catatan AI:** {analisis_ai}"
            
        else:
            pesan = "⚠️ Bot berjalan lancar, tapi data di Spreadsheet masih kosong melompong, Bro."

        # 5. Kirim langsung ke Telegram
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"})
        
        print("✅ Laporan otomatis terbaru sukses terkirim!")

    except Exception as e:
        print(f"❌ Error sistem: {e}")

if __name__ == "__main__":
    lapor_otomatis_v2()
