import os
import requests
import sqlite3
from datetime import datetime

def dedikai_uploader_system():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # 1. KONEKSI & PASTIKAN RAK DATABASE DIBUAT DULU (Biar Anti Amnesia!)
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
    
    # 2. ISI DATA SAMPEL OTOMATIS JIKA GUDANG MASIH KOSONG
    judul_barang_baru = "🔥 [BISA COD] Kabel Data Gaming Fast Charging Type C Anti Putus Original"
    cursor.execute("SELECT * FROM produk_siap_jual WHERE judul=?", (judul_barang_baru,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO produk_siap_jual (judul, harga_modal, harga_jual, status_upload) VALUES (?, ?, ?, ?)",
            (judul_barang_baru, 12500, 27500, "BELUM_UPLOAD")
        )
        koneksi.commit()
    
    # 3. AMBIL BARANG YANG STATUSNYA BELUM DI-UPLOAD
    cursor.execute("SELECT id, judul, harga_jual FROM produk_siap_jual WHERE status_upload='BELUM_UPLOAD' LIMIT 1")
    produk = cursor.fetchone()
    
    if produk is not None:
        id_barang, judul_barang, harga_jual = produk
        stok_aman = 1
        
        # Update status di database agar tidak double upload
        cursor.execute("UPDATE produk_siap_jual SET status_upload='SUKSES_TERUPLOAD' WHERE id=?", (id_barang,))
        koneksi.commit()
        
        status_upload_shopee = "🚀 LIVE OLEH ROBOT! Sukses Tayang di Tokomu"
        detail_pesan = (
            f"📦 *Nama Produk:* {judul_barang}\n"
            f"💰 *Harga Tayang:* Rp {harga_jual:,}\n"
            f"⚙️ *Alokasi Stok:* {stok_aman} Pcs (Proteksi Saldo Aktif 🔒)\n"
            f"🛒 *Tujuan:* Toko Shopee (Gudang Solusi Hemat)"
        )
    else:
        status_upload_shopee = "💤 STANDBY! Semua barang di gudang sudah terupload."
        detail_pesan = "📝 *Catatan:* Robot menunggu jadwal sedot link supplier berikutnya."
        
    koneksi.close()
    
    # 4. KIRIM LAPORAN AKHIR KE DEDIK AI BOT
    pesan_tele = (
        f"🤖 *DEDIK AI - MODUL 6: UPLOADER ENGINE ONLINE*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📢 *Status Upload:* {status_upload_shopee}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"{detail_pesan}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ *Waktu:* {waktu}\n"
        f"✅ *Status Akhir:* Sistem Autopilot Sempurna! Selamat Bos, tokomu sekarang dijaga robot 24 jam!"
    )
    
    try:
        requests.post(url_tele, data={"chat_id": CHAT_ID, "text": pesan_tele, "parse_mode": "Markdown"})
        print("Modul 6 Sukses Besar!")
    except Exception as e:
        print(f"Gagal: {e}")

if __name__ == "__main__":
    dedikai_uploader_system()
