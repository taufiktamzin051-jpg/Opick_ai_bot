import os
import re
import requests
import tweezers # Jika ada typo, pastikan import tweepy yang benar
import tweepy
from telethon import TelegramClient, events

# =========================================================================
# 🔑 1. KONFIGURASI API (DIAMBIL DARI GITHUB SECRETS)
# =========================================================================
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN_TELEGRAM = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_TARGET_TELEGRAM = os.getenv("TELEGRAM_CHAT_ID")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

IA_API_KEY = os.getenv("INVOLVE_ASIA_API_KEY")
IA_SECRET_KEY = os.getenv("INVOLVE_ASIA_SECRET_KEY")

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
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("⚠️ [Twitter] Kunci rahasia Twitter di GitHub Secrets belum lengkap! Skip.")
        return
        
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        
        # Batasi panjang karakter Twitter (Maksimal 280)
        teks_tweet = teks_postingan[:270] + "..." if len(teks_postingan) > 275 else teks_postingan
            
        client.create_tweet(text=teks_tweet)
        print("🐦 [Twitter] BERHASIL! Tweet produk sudah meluncur ke profil X Anda.")
    except Exception as e:
        print(f"❌ [Twitter] Gagal kirim tweet: {e}")

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
# 🧠 5. PROSES UTAMA ROBOT
# =========================================================================
POLA_LINK = r'(https?://(?:s\.shopee\.co\.id|shope\.ee|tokopedia\.link|shopee\.co\.id|tokopedia\.com)[^\s\?]+)'

if not API_ID or not API_HASH:
    print("❌ TELEGRAM_API_ID atau TELEGRAM_API_HASH belum di-set di Secrets!")
    exit(1)

client_pengintai = TelegramClient('session_pengintai', int(API_ID), API_HASH)

@client_pengintai.on(events.NewMessage(chats=GRUP_INTAIAN))
async def tangkap_dan_sebar(event):
    teks_asal = event.message.message
    if not teks_asal:
        return
        
    cari_link = re.findall(POLA_LINK, teks_asal)
    if cari_link:
        link_asli = cari_link[0]
        print(f"\n🔗 Link Produk Ditemukan: {link_asli}")
        
        link_cuan = konversi_ke_link_afiliasi(link_asli)
        teks_bersih = teks_asal.replace(link_asli, "").strip()
        if not teks_bersih:
            teks_bersih = "🔥 Rekomendasi Diskon Spesial Hari Ini! Cek Sekarang Sebelum Habis 👇"
            
        format_postingan = f"{teks_bersih}\n\n👉 Klik Belanja di Sini: {link_cuan}"
        
        # Kirim ke dua platform sekaligus
        kirim_ke_telegram(format_postingan)
        kirim_ke_twitter(format_postingan)

if __name__ == '__main__':
    print("⚡ ROBOT DUET TELEGRAM & TWITTER MULAI DINYALAKAN...")
    client_pengintai.start()
    client_pengintai.run_until_disconnected()
