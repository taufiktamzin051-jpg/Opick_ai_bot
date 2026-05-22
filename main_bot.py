import os
import re
import requests
from bs4 import BeautifulSoup

# 1. Ambil Kunci Rahasia dari GitHub Secrets
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ID_CHAT = os.getenv("TELEGRAM_CHAT_ID")
INVOLVE_API_KEY = os.getenv("INVOLVE_API_KEY")
INVOLVE_SECRET_KEY = os.getenv("INVOLVE_SECRET_KEY")

# 2. DAFTAR 5 GRUP TARGET YANG DIINTAI (Termasuk 3 grup baru Anda)
GRUP_TARGET = [
    "https://t.me/SHOPEE_BIG_SALES",
    "https://t.me/gotokped",
    "https://t.me/Racun_Shopee_Murah_Diskon_Receh",
    "https://t.me/racun_shopee_receh_ss",
    "https://t.me/racun_tokped_receh"
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

def intip_grup_kompetitor(url_grup):
    nama_grup = url_grup.split("/")[-1]
    print(f"🕵️‍♂️ Robot sedang mengintai grup: {nama_grup}")
    try:
        url_preview = f"https://t.me/s/{nama_grup}"
        respon = requests.get(url_preview, headers=headers_web, timeout=15)
        sup = BeautifulSoup(respon.text, 'html.parser')
        
        kotak_pesan = sup.find_all("div", {"class": "tgme_widget_message_bubble"})
        if not kotak_pesan:
            return None, None
            
        pesan_terakhir = kotak_pesan[-1]
        
        komponen_teks = pesan_terakhir.find("div", {"class": "tgme_widget_message_text"})
        teks_asli = komponen_teks.text.strip() if komponen_teks else ""
        
        link_produk_spesifik = None
        semua_link_href = pesan_terakhir.find_all("a")
        
        for link in semua_link_href:
            href_url = link.get("href", "")
            if any(x in href_url for x in ["shopee.co.id", "tokopedia.com", "tokopedia.link", "onelink.me", "t.me/s/"]):
                if f"t.me/{nama_grup}" in href_url or href_url == url_grup:
                    continue
                link_produk_spesifik = href_url
                break
                
        if not link_produk_spesifik and teks_asli:
            links_raw = re.findall(r'(https?://[^\s]+)', teks_asli)
            if links_raw:
                link_produk_spesifik = links_raw[0]
                
        return teks_asli, link_produk_spesifik
    except Exception as e:
        print(f"❌ Gagal mengintai grup {nama_grup}: {e}")
        return None, None

if __name__ == "__main__":
    print("=== ROBOT PENGINTAI MULTI-GRUP BARU START ===")
    
    if not TOKEN or not ID_CHAT:
        print("❌ Eror: Token atau Chat ID tidak lengkap!")
        exit(1)
        
    for grup in GRUP_TARGET:
        pesan_raw, link_asal = intip_grup_kompetitor(grup)
        
        if pesan_raw:
            # Jika ketemu link produk spesifik, otomatis di-convert
            if link_asal:
                print(f"🔗 Link Produk Ditemukan: {link_asal[:50]}...")
                link_final = convert_ke_link_cuan(link_asal)
            else:
                # Logika cadangan dinamis jika tidak ada link produk sama sekali
                print("⚠️ Tidak ada link produk spesifik, menggunakan link toko cadangan.")
                if "tokoped" in grup.lower():
                    link_final = "https://www.tokopedia.com"
                else:
                    link_final = "https://shopee.co.id"
            
            url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            
            # Logika penentu judul otomatis biar sesuai tema grup target Anda
            nama_grup_kecil = grup.lower()
            if "tokoped" in nama_grup_kecil:
                sumber = "TOKOPEDIA SPECIAL DISKON"
            elif "receh" in nama_grup_kecil:
                sumber = "RACUN SHOPEE RECEH"
            elif "shopee" in nama_grup_kecil:
                sumber = "SHOPEE VIRAL HITS"
            else:
                sumber = "REKOMENDASI DISKON TERBARU"
            
            pesan_kirim = (
                f"🔥 {sumber} 🔥\n\n"
                f"{pesan_raw}\n\n"
                f"🛍️ Miliki Produknya Sekarang Di Sini: \n{link_final}"
            )
            
            payload = {
                "chat_id": ID_CHAT,
                "text": pesan_kirim
            }
            
            kirim = requests.post(url_tele, json=payload, timeout=15)
            if kirim.status_code == 200:
                print(f"🚀 Sukses mengirim postingan dari grup: {grup.split('/')[-1]}")
            else:
                print(f"❌ Gagal kirim: {kirim.text}")
            
    print("=== SEMUA PROSES SELESAI ===")
    
