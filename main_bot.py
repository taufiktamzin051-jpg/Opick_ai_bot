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
    print(f"🔗 Mencoba mengonversi link: {link_mentah[:40]}...")
    if not INVOLVE_API_KEY or not INVOLVE_SECRET_KEY:
        print("⚠️ Kunci Involve Asia belum lengkap di GitHub Secrets, menggunakan link asli.")
        return link_mentah

    # API resmi Involve Asia untuk membuat link afiliasi otomatis
    url_api = "https://api.involve.asia/api/v1/deeplink/generate"
    
    payload = {
        "api_key": INVOLVE_API_KEY,
        "secret_key": INVOLVE_SECRET_KEY,
        "url": link_mentah
    }
    
    try:
        respon = requests.post(url_api, json=payload, timeout=15)
        data = respon.json()
        
        # Jika sukses, ambil link afiliasi barunya
        if respon.status_code == 200 and data.get("status") == "success":
            link_afiliasi = data.get("generated_url")
            print("✅ Link berhasil diubah menjadi LINK CUAN!")
            return link_afiliasi
        else:
            print(f"⚠️ Gagal convert API: {data.get('message', 'Eror tidak diketahui')}")
            return link_mentah
    except Exception as e:
        print(f"❌ Terjadi gangguan server API Involve Asia: {e}")
        return link_mentah

def ekstrak_link_asli(teks):
    links = re.findall(r'(https?://[^\s]+)', teks)
    for link in links:
        if "shopee.co.id" in link or "tokopedia.com" in link or "tokopedia.link" in link:
            return link
    return None

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
            print(f"📝 Konten berhasil disalin dari {nama_grup}!")
            link_produk = ekstrak_link_asli(pesan_terakhir)
            return pesan_terakhir, link_produk
        else:
            print(f"❌ Tidak bisa membaca pesan di grup {nama_grup}")
            return None, None
        
    except Exception as e:
        print(f"❌ Gagal mengintai grup {nama_grup}: {e}")
        return None, None

if __name__ == "__main__":
    print("=== ROBOT PENGINTAI + AUTO CUAN START ===")
    
    if not TOKEN or not ID_CHAT:
        print("❌ Eror: Token atau Chat ID tidak lengkap!")
        exit(1)
        
    for grup in GRUP_TARGET:
        konten_pesan, link_asal = intip_grup_kompetitor(grup)
        
        if konten_pesan:
            # Jika ada link produk, otomatis ubah lewat Involve Asia
            if link_asal:
                link_final = convert_ke_link_cuan(link_asal)
            else:
                link_final = "https://tokopedia.com" if "tokoped" in grup else "https://shopee.co.id"
            
            url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            sumber = "TOKOPEDIA HITS" if "tokoped" in grup else "SHOPEE VIRAL"
            
            pesan_kirim = (
                f"🔥 REKOMENDASI {sumber} 🔥\n\n"
                f"{konten_pesan}\n\n"
                f"🛍️ Miliki Produknya Sekarang Di Sini: \n{link_final}"
            )
            
            payload = {
                "chat_id": ID_CHAT,
                "text": pesan_kirim
            }
            
            kirim = requests.post(url_tele, json=payload, timeout=15)
            if kirim.status_code == 200:
                print(f"🚀 Sukses meneruskan postingan ber-afiliasi dari {grup.split('/')[-1]}!")
            else:
                print(f"❌ Gagal kirim ke Telegram: {kirim.text}")
            
    print("=== SEMUA PROSES PENGINTAIAN SELESAI ===")
