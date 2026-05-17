import os
import requests
import google.generativeai as genai

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

    try:
        # Menggunakan model terbaru & paling stabil
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Berikan 1 ide produk rekomendasi unik yang berguna untuk rumah tangga. "
            "Buatlah caption promosi pendek yang menarik dan sertakan emoji. "
            "Sediakan teks '[LINK_PRODUK]' di bagian paling akhir."
        )
        
        response = model.generate_content(prompt)
        caption_hasil = response.text
        
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
