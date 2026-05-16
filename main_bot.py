import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

def lapor_otomatis_penyesuaian():
    # Menggunakan nama rahasia yang sesuai dengan inisial gudang rahasiamu (CH, GC, GE, SP, TE, TO)
    token = os.getenv('TOKEN_TELEGRAM') or os.getenv('TELEGRAM_TOKEN') or os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID_TELEGRAM') or os.getenv('TELEGRAM_CHAT_ID') or os.getenv('CHAT_ID')
    gcp_json = os.getenv('GCP_CREDENTIALS') or os.getenv('KREDENSIAL_GCP') or os.getenv('GCP_JSON')
    sheet_id = os.getenv('SPREADSHEET_ID') or os.getenv('ID_SPREADSHEET') or os.getenv('SHEET_ID')

    waktu_skrg = datetime.now().strftime("%d/%m/%Y %H:%M")
    pesan = ""

    # Deteksi darurat jika ada rahasia kunci yang beneran kosong di GitHub
    if not token or not chat_id:
        print("❌ Kunci TOKEN atau CHAT_ID Telegram tidak ditemukan di Secrets GitHub!")
        return
        
    if not gcp_json or not sheet_id:
        pesan = f"⚠️ **Sistem Aktif Tapi Terbata-bata**\n⏰ {waktu_skrg} WIB\n━━━━━━━━━━━━━━━\n❌ Robot gagal jalan karena nama rahasia Google Sheets (GCP/SPREADSHEET_ID) di Secrets GitHub belum pas nama variabelnya, Bro."
    else:
        try:
            # Akses Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(gcp_json), scope)
            client = gspread.authorize(creds)
            sheet = client.open_by_key(sheet_id).sheet1
            
            semua_baris = sheet.get_all_values()
            
            if len(semua_baris) > 1:
                judul_kolom = semua_baris[0]
                baris_terakhir = semua_baris[-1]
                
                pesan = f"🤖 **LAPORAN TRANSAKSI DEDIK AI**\n"
                pesan += f"⏰ Waktu Cek: {waktu_skrg} WIB\n"
                pesan += f"━━━━━━━━━━━━━━━\n"
                for i in range(len(judul_kolom)):
                    nama_kolom = judul_kolom[i] if judul_kolom[i] else f"Kolom_{i+1}"
                    isi_nilai = baris_terakhir[i] if i < len(baris_terakhir) else "-"
                    pesan += f"📍 **{nama_kolom}**: {isi_nilai}\n"
                pesan += f"━━━━━━━━━━━━━━━\n"
                pesan += f"✅ Laporan Sukses Terkirim, Bos! 🔥"
            else:
                pesan = f"🤖 **SISTEM DEDIK AI AKTIF**\n⏰ {waktu_skrg} WIB\n━━━━━━━━━━━━━━━\n📢 Status: Robot berhasil meronda, tapi isi tabel Google Sheets masih kosong melompong, Bro!"
        except Exception as e:
            pesan = f"❌ **Koneksi Google Sheets Gagal:** Nama rahasia/ID Sheets di GitHub Secrets belum cocok. Eror: {e}"

    # Tembak Laporan ke Telegram
    try:
        url_tele = f"https://api.telegram.org/bot{token}/sendMessage"
        payload_tele = {"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"}
        requests.post(url_tele, json=payload_tele)
        print("🚀 Selesai mengeksekusi pengiriman pesan!")
    except Exception as error_tele:
        print(f"❌ Gagal kontak Telegram: {error_tele}")

if __name__ == "__main__":
    lapor_otomatis_penyesuaian()
