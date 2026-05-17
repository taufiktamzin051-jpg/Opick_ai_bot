import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

def dedikai_database_system():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # 1. SETUP GUDANG DATA (SQLite Database)
    # Membuat file gudang bernama 'gudang_dropship.db' otomatis
    koneksi = sqlite3.connect("gudang_dropship.db")
    cursor = koneksi.cursor()
    
    # Membuat tabel rak barang jika belum ada
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

    # 2. DATA PRODUK YANG DISEDOT
    judul_produk = "🔥 [BISA COD] Kabel Data Gaming Fast Charging Type C Anti Putus Original"
    harga_supplier = 12500
    harga_jual_kamu = 27500
    
    # 3. LOGIKA CEK DATABASE: Biar robot tidak menyedot barang yang sama dua kali
    cursor.execute("SELECT * FROM produk_siap_jual WHERE judul=?", (judul_produk,))
    data_lama = cursor.fetchone()
    
    if data_lama is None:
        # Jika barang baru, masukkan ke dalam gudang database
        cursor.execute(
            "INSERT INTO produk_siap_jual (judul, harga_modal, harga_jual, status_upload) VALUES (?, ?, ?, ?)",
            (judul_produk, harga_supplier, harga_jual_kamu, "BELUM_UPLOAD")
        )
        koneksi.commit()
        status_db = "🆕 Sukses Tersimpan di Gudang Database!"
    else:
        status_db = "🔄 Barang sudah ada di gudang, dilewati biar hemat memori!"
        
    koneksi.close()
    
    # 4. LAPORAN KE DEDIK AI BOT
    pesan_tele = (
        f"🤖 *DEDIK AI - MODUL 4: DATABASE ENGINE ACTIVE*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📦 *Produk:* {judul_produk}\n"
        f"💰 *Harga Jual:* Rp {harga_jual_kamu:,}\n"
        f"🗄️ *Gudang DB:* {status_db}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ *Waktu:* {waktu}\n"
        f"✅ *Status:* Data aman di database! Langkah selanjutnya: mengaktifkan modul pelempar otomatis ke tokomu."
    )
    
    try:
        requests.post(url_tele, data={"chat_id": CHAT_ID, "text": pesan_tele, "parse_mode": "Markdown"})
        print("Modul 4 Berhasil!")
    except Exception as e:
        print(f"Gagal: {e}")

if __name__ == "__main__":
    dedikai_database_system()
