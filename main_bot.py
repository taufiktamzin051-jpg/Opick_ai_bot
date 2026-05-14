
import os
import requests

def kirim_test():
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Pesan yang akan dikirim
    teks = "🚀 DEDIK AI: Koneksi Berhasil! Jika Anda membaca ini, berarti bot sudah benar."
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": teks}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ BERHASIL: Pesan terkirim ke Telegram!")
        else:
            print(f"❌ GAGAL: Kode status {response.status_code}")
            print(f"Pesan Error: {response.text}")
    except Exception as e:
        print(f"⚠️ ERROR SISTEM: {e}")

if __name__ == "__main__":
    kirim_test()
