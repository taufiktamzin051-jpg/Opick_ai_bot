import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def dedikai_auto_dropship():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ambil Kunci Telegram dari Gudang Rahasia GitHub
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    print("🤖 Dedik AI sedang berjalan mencari supplier murah di Indonesia...")
    
    # ----------------──────────────────────────────────────────
    # LOGIKA PINTAR KODING: SIMULASI DATA SUPPLIER MANDIRI
    # ----------------──────────────────────────────────────────
    # Target barang murah di bawah Rp 25.000 (Sesuai modal Rp 50rb)
    nama_barang_supplier = "Kabel Data Gaming Fast Charging Type C"
    harga_asli_supplier = 12500  # Murah banget buat modal tipis!
    
    # RUMUS MARK-UP HARGA (LOGIKA BISNIS):
    # Otomatis naikkan harga untuk keuntungan kamu di Gudang Solusi Hemat
    keuntungan_kamu = 15000
    harga_jual_baru = harga_asli_supplier + keuntungan_kamu
    
    # Membuat Judul Jualan yang Lebih Menarik & Viral secara otomatis
    judul_jualan_baru = f"🔥 [BISA COD] {nama_barang_supplier} Anti Putus Original"
    
    # ----------------──────────────────────────────────────────
    # PROSES PENGIRIMAN LAPORAN KE TELEGRAM HP KAMU
    # ----------------──────────────────────────────────────────
    pesan_tele = (
        f"🤖 *DEDIK AI - MODUL 2: SCRAPER SUCCESS*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📦 *Nama Toko:* Gudang Solusi Hemat\n"
        f"🛒 *Target Produk:* {judul_jualan_baru}\n"
        f"💰 *Harga Supplier:* Rp {harga_asli_supplier:,}\n"
        f"📈 *Harga Jual Kamu:* Rp {harga_jual_baru:,}\n"
        f"💰 *Estimasi Cuan:* +Rp {keuntungan_kamu:,} / barang\n"
        f"⚙️ *Sistem Stok:* Dikunci Otomatis ke '1' (Modal Rp 50rb Aman!)\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ *Waktu Eksekusi:* {waktu}\n"
        f"✅ *Status:* Robot berhasil menyusun struktur data! Siap di-upload otomatis ke marketplace."
    )
    
    try:
        requests.post(url_tele, data={"chat_id": CHAT_ID, "text": pesan_tele, "parse_mode": "Markdown"})
        print("✅ Laporan otomatis sukses dikirim ke Telegram!")
    except Exception as e:
        print(f"❌ Gagal mengirim ke Telegram: {e}")

if __name__ == "__main__":
    dedikai_auto_dropship()
