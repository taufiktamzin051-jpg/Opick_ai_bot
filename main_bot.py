import os
import requests
from bs4 import BeautifulSoup

# 1. Ambil Token & ID Obrolan dari Brankas GitHub Secrets
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ID_CHAT = os.getenv("TELEGRAM_CHAT_ID")

# 2. Link Supplier Tokopedia Punya Bos Taufik
TARGET_TAUTAN = "https://tk.tokopedia.com/ZS" # (Sesuaikan dengan kelanjutan link asli Anda)

print("🤖 Robot mulai nge-scrape Tokopedia...")

# Headers ringkas biar gak mudah diblokir
judul = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # Ambil halaman web Tokopedia
    menanggapi = requests.get(TARGET_TAUTAN, headers=judul, timeout=15)
    sup = BeautifulSoup(menanggapi.text, 'html.parser')
    
    # Ambil Nama Produk
    el_judul = sup.find("h1", {"data-testid": "lblPDPProductName"})
    nama_barang = el_judul.text.strip() if el_judul else "Produk Afiliasi"
    
    # Ambil Harga Modal Supplier
    el_harga = sup.find("div", {"data-testid": "lblPDPProductPrice"})
    harga_modal = el_harga.text.strip() if el_harga else "Cek Harga"
    
    status_bot = "AKTIF SECARA REAL-TIME 🟢"

except Exception as e:
    # Kalau internet eror atau diblokir, otomatis pakai data cadangan
    print(f"Ada kendala scrape: {e}")
    nama_barang = "Kabel Data Pengisian Cepat"
    harga_modal = "10750"
    status_bot = "MODE CADANGAN (AMAN) 🟡"

# 3. Kirim Hasil ke Telegram
if TOKEN and ID_CHAT:
    url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    pesan = (
        f"📢 *LAPORAN BOT AFILIASI* ({status_bot})\n\n"
        f"📦 *Nama Barang:* {nama_barang}\n"
        f"💰 *Harga Modal:* {harga_modal}\n\n"
        f"🔗 *Link Produk:* {TARGET_TAUTAN}"
    )
    payload = {
        "chat_id": ID_CHAT,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    requests.post(url_tele, json=payload, timeout=15)
    print("🚀 Sukses kirim ke Telegram!")
else:
    print("❌ Eror: Token Telegram atau Chat ID belum diset di GitHub Secrets!")
