import os
import requests

# 1. SETUP KONFIGURASI
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")

def jalankan_robot_affiliate():
    print("Mulai menjalankan robot...")
    if not GEMINI_KEY:
        kirim_telegram("❌ Kunci GEMINI_API_KEY tidak ditemukan di Secrets!")
        return

    # KUNCI ANTI-GAGAL: Menggunakan API Web Langsung tanpa Library Google
    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt = (
        "Berikan 1 ide produk rekomendasi unik yang berguna untuk rumah tangga. "
        "Buatlah caption promosi pendek yang menarik di Twitter dan sertakan emoji. "
        "Sediakan teks '[LINK_PRODUK]' di bagian paling akhir."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url_gemini, headers=headers, json=payload)
        response_data = response.json()
        
        # Mengambil teks hasil generate AI
        caption_hasil = response_data['candidates'][0]['content']['parts'][0]['text']
        
        link_affiliate = "https://amzn.to/3WbXyz"
        caption_final = caption_hasil.replace("[LINK_PRODUK]", link_affiliate)
        
        laporan = f"🤖 *Laporan Konten Baru AI:*\n\n{caption_final}"
        kirim_telegram(laporan)
        print("Berhasil mengirim ke Telegram!")
        
    except Exception as e:
        error_msg = f"❌ Terjadi kesalahan robot: {str(e)}"
        print(error_msg)
        kirim_telegram(error_msg)

if __name__ == "__main__":
    jalankan_robot_affiliate()
