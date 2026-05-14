import os
import requests

def kirim_telegram(pesan):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {"chat_id": chat_id, "text": pesan}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("✅ PESAN MASUK KE TELEGRAM!")
    else:
        print(f"❌ ERROR: {response.text}")

if __name__ == "__main__":
    kirim_telegram("🚀 Dedik AI Berhasil Aktif!")
