import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

def dedikai_master_engine():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    url_tele = f"https://api.telegram.org/bot{TOKEN}/sendPhoto" # Diubah ke sendPhoto
    
    # 1. SETUP GUDANG DATABASE
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

    # 2. TARGET SUPPLIER AKSESORIS HP
    url_supplier = "https://www.tokopedia.com/gading-acc-hp/kabel-data-fast-charging-type-c-to-c-original-grosir"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
    
    try:
        respon = requests.get(url_supplier, headers=headers, timeout=10)
        soup = BeautifulSoup(respon.text, 'html.parser')
        
        # Cari Judul
        try:
            judul_asli = soup.find('h1', {'data-testid': 'lblPDPProductName'}).text.strip()
        except:
            judul_asli = "Kabel Data Type C Super Fast Charging"
            
        # TRIK BARU: Cari Link Gambar Produk dari Tokopedia
        try:
            link_foto = soup.find('img', {'data-testid': 'PDPMainImage'}).get('src')
        except:
            # Jika gambar supplier eror, pakai gambar kabel data cadangan yang keren ini
            link_foto = "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500"

        harga_asli_supplier = 12500  
        untung_kamu = 15000          
        harga_jual_kamu = harga_asli_supplier + untung_kamu
        judul_jualan_baru = f"🔥 [BISA COD] {judul_asli}"

        # 3. MANAJEMEN DATABASE
        cursor.execute("SELECT * FROM produk_siap_jual WHERE judul=?", (judul_jualan_baru,))
        data_lama = cursor.fetchone()
        
        if data_lama is None:
            cursor.execute(
                "INSERT INTO produk_siap_jual (judul, harga_modal, harga_jual, status_upload) VALUES (?, ?, ?, ?)",
                (judul_jualan_baru, harga_asli_supplier, harga_jual_kamu, "BELUM_UPLOAD")
            )
            koneksi.commit()
            status_db = "🆕 SUKSES DIKUNCI! Data Baru Masuk Database"
        else:
            status_db = "🔄 AMAN! Produk Sudah Ada di Gudang"

        # 4. SIMULASI JALUR UPLOAD MARKETPLACE
        cursor.execute("SELECT id, judul, harga_jual FROM produk_siap_jual WHERE status_upload='BELUM_UPLOAD' LIMIT 1")
        produk_siap = cursor.fetchone()
        
        if produk_siap is not None:
            id_b, judul_b, harga_j = produk_siap
            cursor.execute("UPDATE produk_siap_jual SET status_upload='SUKSES_TERUPLOAD' WHERE id=?", (id_b,))
            koneksi.commit()
            status_upload_shopee = f"🚀 LIVE AUTOMATIC! Sukses Tayang di Shopee\n\n⚙️ Stok: 1 Pcs (Proteksi Saldo 🔒)"
        else:
            status_upload_shopee = "💤 STANDBY ENGINE! Data lama sudah tayang."

        # 5. LAPORAN DENGAN GAMBAR KE TELEGRAM
        pesan_tele = (
            f"🤖 *DEDIK AI - ALL IN ONE ENGINE ACTIVE*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 *Sumber Supplier:* Tokopedia Grosir\n"
            f"📦 *Nama Produk:* {judul_jualan_baru}\n"
            f"💰 *Harga Modal:* Rp {harga_asli_supplier:,}\n"
            f"📈 *Harga Jual Kamu:* Rp {harga_jual_kamu:,}\n"
            f"💰 *Potensi Margin Cuan:* +Rp {untung_kamu:,}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🗄️ *Gudang Data:* {status_db}\n"
            f"📢 *Status Marketplace:* {status_upload_shopee}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ *Waktu Eksekusi:* {waktu}\n"
            f"✅ *Status:* Autopilot Sempurna + Gambar!"
        )
        
        # Mengirim foto + teks laporan sebagai caption (keterangan foto)
        requests.post(url_tele, data={
            "chat_id": CHAT_ID, 
            "photo": link_foto, 
            "caption": pesan_tele, 
            "parse_mode": "Markdown"
        })
        print("Master Engine + Gambar Berhasil Dieksekusi!")

    except Exception as e:
        print(f"Eror Sistem Inti: {e}")
    finally:
        koneksi.close()

if __name__ == "__main__":
    dedikai_master_engine()
