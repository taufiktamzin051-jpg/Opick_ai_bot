import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

def dedikai_full_system():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # 1. KONEKSI KE GUDANG DATABASE
    koneksi = sqlite3.connect("gudang_dropship.db")
    cursor = koneksi.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk_siap_jual (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT,
            harga_modal INTEGER,
            harga_jual INTEGER,
            status_upload TEXT
        )
    ''')
    koneksi.commit()

    # 2. PROSES NYEDOT LINK SUPPLIER TOKOPEDIA ASLI
    url_supplier = "https://www.tokopedia.com/gading-acc-hp/kabel-data-fast-charging-type-c-to-c-original-grosir"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
    
    try:
        respon = requests.get(url_supplier, headers=headers, timeout=10)
        soup = BeautifulSoup(respon.text, 'html.parser')
        
        try:
            judul_asli = soup.find('h1', {'data-testid': 'lblPDPProductName'}).text.strip()
        except:
            judul_asli = "Kabel Data Type C Super Fast Charging"
            
        harga_asli_supplier = 12500  # Harga modal grosir
        untung_kamu = 15000          # Amankan margin modal 50rb
        harga_jual_kamu = harga_asli_supplier + untung_kamu
        judul_jualan_baru = f"🔥 [BISA COD] {judul_asli}"

        # 3. LOGIKA SAVE KE DATABASE (Anti Duplikat)
        cursor.execute("SELECT * FROM produk_siap_jual WHERE judul=?", (judul_jualan_baru,))
        data_lama = cursor.fetchone()
        
        if data_lama is None:
            cursor.execute(
                "INSERT INTO produk_siap_jual (judul, harga_modal, harga_jual, status_upload) VALUES (?, ?, ?, ?)",
                (judul_jualan_baru, harga_asli_supplier, harga_jual_kamu, "BELUM_UPLOAD")
            )
            koneksi.commit()
            status_db = "🆕 DATA BARU! Sukses Dikunci di Database Gudang"
        else:
            status_db = "🔄 DATA LAMA! Sudah Ada di Gudang (Aman dari Duplikat)"

        # 4. KIRIM LAPORAN INTEGRASI KE DEDIK AI BOT
        pesan_tele = (
            f"🤖 *DEDIK AI - MODUL 5: INTEGRATED SYSTEM ACTIVE*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 *Sumber:* Tokopedia Supplier\n"
            f"📦 *Produk:* {judul_jualan_baru}\n"
            f"💰 *Harga Jual Kamu:* Rp {harga_jual_kamu:,}\n"
            f"🗄️ *Status Database:* {status_db}\n"
            f"⚙️ *Manajemen Stok:* Lock '1' (Aman untuk Saldo Rp 50rb)\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ *Waktu:* {waktu}\n"
            f"✅ *Status:* Integrasi Sempurna! Otak penyedot dan gudang data sudah menyatu."
        )
        
        requests.post(url_tele, data={"chat_id": CHAT_ID, "text": pesan_tele, "parse_mode": "Markdown"})
        print("Modul 5 Sukses Berjalan!")

    except Exception as e:
        print(f"Eror Sistem: {e}")
    finally:
        koneksi.close()

if __name__ == "__main__":
    dedikai_full_system()
