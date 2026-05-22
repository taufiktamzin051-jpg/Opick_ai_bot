import os
import re
import requests
from bs4 import BeautifulSoup

# 1. Ambil Kunci Rahasia dari GitHub Secrets
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ID_CHAT = os.getenv("TELEGRAM_CHAT_ID")
INVOLVE_API_KEY = os.getenv("INVOLVE_API_KEY")
INVOLVE_SECRET_KEY = os.getenv("INVOLVE_SECRET_KEY")

# 2. DAFTAR GRUP TARGET YANG DIINTAI
GRUP_TARGET = [
    "https://t.me/SHOPEE_BIG_SALES",
    "https://t.me/gotokped"
]

headers_web = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def convert_ke_link_cuan(link_mentah):
    if not INVOLVE_API_KEY or not INVOLVE_SECRET_KEY:
        return link_mentah

    url_api = "https://api.involve.asia/api/v1/deeplink/generate"
    payload = {
        "api_key": INVOLVE_API_KEY,
        "secret_key": INVOLVE_SECRET_KEY,
        "url": link_mentah
    }
    
    try:
        respon = requests.post(url_api, json=payload, timeout=15)
        data = respon.json()
        if respon.status_code == 200 and data.get("status") == "success":
            return data.get("generated_url")
        return link_mentah
    except:
        return link_mentah

def proses_dan_ubah_semua_link(teks, url_grup):
    # Cari semua link di dalam teks asli
    links = re.findall(r'(https?://[^\s]+)', teks)
    link_terubah = None
    
    for link in links:
        # Cek apakah ini link marketplace yang mau di-convert
        if any(x in link for x in ["shopee.co.id", "tokopedia.com", "tokopedia.link", "onelink.me"]):
            link_cuan = convert_ke_link_cuan(link)
            teks = teks.replace(link, link_cuan)
            link_terubah = link_cuan
            
    # JIKA TIDAK ADA LINK SAMA SEKALI DI TEKS:
    # Setel link cadangan otomatis menyesuaikan asal grupnya agar tidak tertukar
    if not link_terubah:
        if "tokoped" in url_grup:
            link_terubah = "https://www.tokopedia.com"
        else:
            link_terubah = "https://shopee.co.id"
            
    return teks, link_terubah

def intip_grup_kompetitor(url_grup):
    nama_grup = url_grup.split("/")[-1]
    print(f"🕵️‍♂️ Robot sedang mengintai grup: {nama_grup}")
    try:
        url_preview = f"https://t.me/s/{nama_grup}"
        respon = requests.get(url_preview, headers=headers_web, timeout=15)
        sup = BeautifulSoup(respon.text, 'html.parser')
        pesan_pesan = sup.find_all("div", {"class": "tgme_widget_message_text"})
        
        if pesan_pesan:
            pesan_terakhir = pesan_pesan[-1].text.strip()
            return pesan_terakhir
        return None
    except Exception as e:
        print(f"❌ Gagal mengintai grup {nama_grup}: {e}")
        return None

if __name__ == "__main__":
    print("=== ROBOT PENGINTAI FIX CHAT ID + LOGIKA CADANGAN START ===")
    
    if not TOKEN or not ID_CHAT:
        print("❌ Eror: Token atau Chat ID tidak lengkap!")
        exit(1)
        
    for grup in GRUP_TARGET:
        pesan_raw = intip_grup_kompetitor(grup)
        
        if pesan_raw:
            # Olah teks dan ubah semua link mentah yang ada di dalamnya
            pesan_final, link_tombol = proses_dan_ubah_semua_link(pesan_raw, grup)
            
            url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            sumber = "TOKOPEDIA HITS" if "tokoped" in grup else "SHOPEE VIRAL"
            
            pesan_kirim = (
                f"🔥 REKOMENDASI {sumber} 🔥\n\n"
                f"{pesan_final}\n\n"
                f"🛍️ Miliki Produknya Sekarang Di Sini: \n{link_tombol}"
            )
            
            payload = {
                "chat_id": ID_CHAT,
                "text": pesan_kirim
            }
            
            kirim = requests.post(url_tele, json=payload, timeout=15)
            if kirim.status_code == 200:
                print(f"🚀 Sukses mengirim postingan ber-afiliasi ke ID: {ID_CHAT}")
            else:
                print(f"❌ Gagal kirim: {kirim.text}")
            
    print("=== SEMUA PROSES SELESAI ===")
