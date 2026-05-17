import os
import requests
import google.generativeai as genai
import tweepy

# 1. SETUP KONFIGURASI (Mengambil dari GitHub Secrets)
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")

# 2. FUNGSI KIRIM NOTIFIKASI TELEGRAM
def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")

# 3. KODE UTAMA ROBOT RUNNING
def jalankan_robot_affiliate():
    print("Robot Affiliate Global Mulai Bekerja...")
    
    if not GEMINI_KEY:
        kirim_telegram("❌ Robot Berhenti: GEMINI_API_KEY belum diisi di GitHub Secrets!")
        return
        
    try:
        # Menggunakan model terbaru agar tidak error 404 lagi
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Berikan 1 ide produk rekomendasi luar negeri yang sedang tren atau sangat berguna untuk rumah tangga/gadget. "
            "Buatlah caption promosi X (Twitter) yang sangat menarik, interaktif, soft-selling, dan sertakan emoji. "
            "Berikan ruang kosong di akhir caption dengan teks '[LINK_PRODUK]' agar saya bisa menaruh link affiliate nanti. "
            "Jangan berikan teks tambahan, cukup berikan caption siap tweet saja."
        )
        
        response = model.generate_content(prompt)
        caption_hasil_ai = response.text
        
        # Simulasi link affiliate
        link_affiliate = "https://amzn.to/3WbXyz" 
        caption_final = caption_hasil_ai.replace("[LINK_PRODUK]", link_affiliate)
        
        print("\n--- HASIL CAPTION GEMINI AI ---")
        print(caption_final)
        
        # 4. POSTING OTOMATIS KE TWITTER/X (Opsional)
        if X_API_KEY and X_API_SECRET and X_ACCESS_TOKEN and X_ACCESS_SECRET:
            client = tweepy.Client(
                consumer_key=X_API_KEY, consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_SECRET
            )
            client.create_tweet(text=caption_final)
            status_x = "✅ Sukses otomatis terposting di Twitter/X!"
        else:
            status_x = "⚠️ Twitter/X dilewati (X API Secrets belum diisi lengkap)."

        # Kirim laporan sukses ke Telegram Anda
        laporan = f"🤖 *Laporan Robot Affiliate*\n\n{status_x}\n\n*Konten Generasi AI:*\n{caption_final}"
        kirim_telegram(laporan)
        
    except Exception as e:
        error_msg = f"❌ Robot Mengalami Error: {str(e)}"
        print(error_msg)
        kirim_telegram(error_msg)

if __name__ == "__main__":
    jalankan_robot_affiliate()
