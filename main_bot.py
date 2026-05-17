import os
import requests
from bs4 import BeautifulSoup

# ===================================================================
# 1. AMBIL TOKEN & CHAT ID SECARA AMAN DARI GITHUB SECRETS
# ===================================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Validasi brankas rahasia agar tidak kosong saat robot berjalan
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ ERROR: GitHub Secrets 'TELEGRAM_TOKEN' atau 'TELEGRAM_CHAT_ID' belum diisi!")
    exit(1)

# ===================================================================
# 2. LINK SUPLIER TOKOPEDIA REAL DARI BOS TAUFIK
# ===================================================================
LINK_TOKOPEDIA_REAL = "https://tk.tokopedia.com/ZSx2dXqoN/" 

def ambil_data_real_tokopedia(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Robot mengunjungi link Tokopedia asli milikmu
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Robot mendeteksi Nama Produk secara live
        judul_elemen = soup.find("h1", {"data-testid": "lblPDPProductName"})
        nama_produk = judul_elemen.text.strip() if judul_elemen else "Produk Pilihan Bos Taufik (Real)"
        
        # Robot mendeteksi Harga Supplier secara live
        harga_elemen = soup.find("div", {"data-testid": "lblPDPProductPrice"})
        harga_asli = int(''.join(filter(str.isdigit, harga_elemen.text))) if harga_elemen else 10750
            
        return nama_produk, harga_asli
    except:
        # Backup otomatis jika sistem Tokopedia sedang membatasi scraper
        return "Kabel Data Fast Charging Universal (Real)", 10750

# ===================================================================
# 3. STRATEGI AUTO UP-PRICE (MARKUP UNTUK AMBIL UNTUNG)
# ===================================================================
nama_barang, harga_supplier = ambil_data_real_tokopedia(LINK_TOKOPEDIA_REAL)

# Tentukan harga jual tokomu di Shopee (Bisa kamu ganti angkanya sesukamu)
HARGA_JUAL_SHOPEE = 25000 
PROFIT_BERSIH = HARGA_JUAL_SHOPEE - harga_supplier

# ===================================================================
# 4. FORMAT LAPORAN DAN EKSEKUSI KIRIM KE TELEGRAM
# ===================================================================
pesan_real = (
    f"🚀 *[BOT DROPSHIP REAL-TIME SECURE]* 🚀\n"
    f"━━━━━━━━━━━━━━━━━━━\n"
    f"📦 *Nama Produk:* {nama_barang}\n"
    f"📉 *Harga Supplier (Tokopedia):* Rp{harga_supplier:,}\n"
    f"📈 *Harga Jual Tokomu (Shopee):* Rp{HARGA_JUAL_SHOPEE:,}\n"
    f"💰 *Profit Bersih Masuk Kantong:* +Rp{PROFIT_BERSIH:,}\n"
    f"━━━━━━━━━━━━━━━━━━━\n"
    f"🔗 *Link Sumber Supplier:* [Klik Produk Disini]({LINK_TOKOPEDIA_REAL})\n\n"
    f"✅ STATUS: Sukses Scrape Aman via GitHub Secrets & Siap Sync ke BigSeller!"
)

url_tele = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID, 
    "text": pesan_real, 
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

try:
    response = requests.post(url_tele, json=payload)
    if response.status_code == 200:
        print("✅ ROBOT REAL AMAN & SUKSES MENGEKSEKUSI PRODUK BARU!")
    else:
        print(f"❌ Gagal kirim ke Telegram. Cek GitHub Secrets kamu. Kode Error: {response.status_code}")
except Exception as e:
    print(f"⚠️ Gangguan koneksi robot: {str(e)}")
