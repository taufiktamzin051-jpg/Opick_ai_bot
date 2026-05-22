import os
import re
import requests
from bs4 import BeautifulSoup

# 1. Ambil Kunci Rahasia dari GitHub Secrets
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ID_CHAT = os.getenv("TELEGRAM_CHAT_ID")

# 2. DAFTAR GRUP TARGET YANG DIINTAI
GRUP_TARGET = [
    "https://t.me/SHOPEE_BIG_SALES",
    "https://t.me/gotokped"
]

judul = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

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
        # Gunakan jalur preview publik resmi Telegram agar pesan selalu terbaca
        url_preview = f"https://t.me/s/{nama_grup}"
        respon = requests.get(url_preview, headers=judul, timeout=15)
        sup = BeautifulSoup(respon.text, 'html.parser')
        
        # Cari semua teks pesan yang tersedia di halaman preview
        pesan_pesan = sup.find_all("div", {"class": "tgme_widget_message_text"})
        
        if not pesan_pesan:
            print(f"📭 Halaman web kosong, mencoba jalur alternatif untuk {nama_grup}...")
            respon = requests.get(url_grup, headers=judul, timeout=15)
            sup = BeautifulSoup(respon.text, 'html.parser')
            pesan_pesan = sup.find_all("div", {"class": "tgme_widget_message_text"})
            
        if pesan_pesan:
            # Ambil pesan paling terakhir yang ada di grup (paling bawah)
            pesan_terakhir = pesan_pesan[-1].text.strip()
            print(f"📝 Konten berhasil disalin: {pesan_terakhir[:50]}...")
            link_produk = ekstrak_link_asli(pesan_terakhir)
            return pesan_terakhir, link_produk
        else:
            print(f"❌ Tetap tidak bisa membaca pesan di grup {nama_grup}")
            return None, None
        
    except Exception as e:
        print(f"❌ Gagal mengintai grup {nama_grup}: {e}")
        return None, None

if __name__ == "__main__":
    print("=== ROBOT PENGINTAI MULTI-MARKETPLACE START ===")
    
    if not TOKEN or not ID_CHAT:
        print("❌ Eror: Token atau Chat ID belum diisi di GitHub Secrets!")
        exit(1)
        
    for grup in GRUP_TARGET:
        konten_pesan, link_asal = intip_grup_kompetitor(grup)
        
        if konten_pesan:
            if not link_asal:
                link_final = "https://tokopedia.com" if "tokoped" in grup else "https://shopee.co.id"
            else:
                link_final = link_asal
            
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
                print(f"🚀 Sukses meneruskan postingan dari {grup.split('/')[-1]}!")
            else:
                print(f"❌ Gagal kirim ke Telegram Anda: {kirim.text}")
            
    print("=== SEMUA PROSES PENGINTAIAN SELESAI ===")
