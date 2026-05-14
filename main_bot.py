import os
import requests

def kirim_telegram(pesan):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    # Kirim pesan teks biasa tanpa format rumit
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": pesan}
    requests.post(url, json=payload)

if __name__ == "__main__":
    kirim_telegram("Halo! Dedik AI sudah terhubung dengan benar.")
