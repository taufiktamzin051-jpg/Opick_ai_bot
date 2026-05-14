import os
import requests

def debug_kirim():
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Cek apakah token terbaca
    if not token:
        print("❌ ERROR: TELEGRAM_TOKEN tidak ditemukan di Secrets GitHub!")
        return

    # Tampilkan debug singkat (aman)
    print(f"DEBUG: Token terbaca sepanjang {len(token)} karakter")
    print(f"DEBUG: Awal token: {token[:4]}... Akhir token: ...{token[-4:]}")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": "Tes terakhir dari GitHub!"}
    
    response = requests.post(url, json=payload)
    print(f"HASIL: {response.status_code} - {response.text}")

if __name__ == "__main__":
    debug_kirim()
    
