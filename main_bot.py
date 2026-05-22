import os
import re
import requests
import tweepy
from telethon import TelegramClient, events

# =========================================================================
# 🔑 1. KONFIGURASI API (OTOMATIS DIAMBIL DARI GITHUB SECRETS)
# =========================================================================
# Kunci Telegram Pengintai
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN_TELEGRAM = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_TARGET_TELEGRAM = os.getenv("TELEGRAM_CHAT_ID") # Channel jualan Anda

# Kunci Twitter (X) Developer API v2
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Kunci Involve Asia (Untuk ubah link otomatis jadi duit)
IA_API_KEY = os.getenv("INVOLVE_ASIA_API_KEY")
IA_SECRET_KEY = os.getenv("INVOLVE_ASIA_SECRET_KEY")

# Daftar username group/channel Telegram murah yang diintai bot Anda
GRUP_INTAIAN = [
    'gotokped',
    'Racun_Shopee_Murah_Diskon_Receh',
    'racun_shopee_receh_ss',
    'racun_tokped_receh'
]

# =========================================================================
# 🚀 2. FUNGSI UNTUK MENGIRIM POSTINGAN KE TWITTER (X)
# =========================================================================
def kirim_ke_twitter(teks_postingan):
    # Validasi apakah kunci Twitter lengkap
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("⚠️ [Twitter] Kunci rahasia Twitter di GitHub Secrets belum lengkap! Skip.")
        return
        
    try:
        # Memakai Tweepy Client khusus API v2 (Gratis / Free Tier)
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        
        # Sifat Twitter terbatas 280 karakter, kita potong jika kepanjangan
        if len(teks_postingan) > 275:
            teks_tweet = teks_postingan[:270] + "..."
        else:
            teks_tweet = teks_postingan
            
        client.create_tweet(text=teks_tweet)
        print("🐦 [Twitter] BERHASIL! Tweet produk sudah meluncur ke profil Anda.")
    except Exception as e:
        print(f"❌ [Twitter] Gagal kirim tweet. Detail kendala: {e}")

# =========================================================================
# 📢 3. FUNGSI UNTUK MENGIRIM POSTINGAN KE TELEGRAM
# =========================================================================
def kirim_ke_telegram(teks_postingan):
    url = f"https://api.telegram.com/bot{BOT_TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHANNEL_TARGET_TELEGRAM,
        "text": teks_postingan,
        "parse_mode": "Markdown"
    }
    try:
        respon = requests.post(url, json=payload)
        if respon.status_code == 200:
            print("📢 [Telegram] BERHASIL! Pesan masuk ke Channel Anda.")
        else:
            print(f"❌ [Telegram] Gagal kirim pesan: {respon.text}")
    except Exception as e:
        print(f"❌ [Telegram] Eror koneksi: {e}")

# =========================================================================
# 💰 4. FUNGSI MEREPACK LINK MENJADI LINK AFILIASI INVOLVE ASIA
# =========================================================================
def konversi_ke_link_afiliasi(link_asli):
    # Jika kunci IA tidak ada, kirim link asli saja sebagai pengaman
    if not IA_API_KEY or not IA_SECRET_KEY:
        return link_asli
        
    url_ia = "https://api.involve.asia/api/v1/deeplink/generate"
    payload = {"url": link_asli}
    headers = {"Authorization": f"Basic {IA_API_KEY}:{IA_SECRET_KEY}"}
    
    try:
        respon = requests.post(url_ia, json=payload, headers=headers)
        if respon.status_code == 200:
            return respon.json().get('deeplink', link_asli)
    except:
        pass
    return link_asli

# =========================================================================
# 🧠 5. PROSES UTAMA ROBOT MENGINTAI DAN MENYEBARKAN LUAPAN CUAN
# =========================================================================
# Pola pencarian link belanja Shopee, Tokopedia, Lazada, dll
POLA_LINK = r'(https?://(?:s\.shopee\.co\.id|shope\.ee|tokopedia\.link|shopee\.co\.id|tokopedia\.com)[^\s\?]+)'

client_pengintai = TelegramClient('session_pengintai', API_ID, API_HASH)

@client_pengintai.on(events.NewMessage(chats=GRUP_INTAIAN))
async def tangkap_dan_sebar(event):
    teks_asal = event.message.message
    if not teks_asal:
        return
        
    cari_link = re.findall(POLA_LINK, teks_asal)
    if cari_link:
        link_asli = cari_link[0]
        print(f"\n🔗 Link Produk Ditemukan: {link_asli}")
        
        # 1. Ubah jadi link komisi milik Anda sendiri
        link_cuan = konversi_ke_link_afiliasi(link_asli)
        
        # 2. Ambil teks deskripsinya saja (buang link lamanya)
        teks_bersih = teks_asal.replace(link_asli, "").strip()
        if not teks_bersih:
            teks_bersih = "🔥 Rekomendasi Diskon Spesial Hari Ini! Cek Sekarang Sebelum Habis 👇"
            
        # 3. Rakit format postingan baru yang rapi
        format_postingan = f"{teks_bersih}\n\n👉 Klik Belanja di Sini: {link_cuan}"
        
        # 4. DUET MAUT: Kirim ke Telegram sekaligus Twitter sekaligus!
        kirim_ke_telegram(format_postingan)
        kirim_ke_twitter(format_postingan)

# Jalankan robot pengintai
if __name__ == '__main__':
    print("⚡ ROBOT DUET TELEGRAM & TWITTER MULAI DINYALAKAN... MENGINTAI GRUP...")
    client_pengintai.start()
    client_pengintai.run_until_disconnected()
