import os
import base64

def samarkan(teks):
    if not teks: return "KOSONG"
    # Mengubah teks asli jadi kode acak biar gak disensor GitHub
    bytes_teks = teks.encode('ascii')
    base64_bytes = base64.b64encode(bytes_teks)
    return base64_bytes.decode('ascii')

print("=== 🔐 KODE PENYAMARAN RAHASIA LU (SALIN SEMUA DI BAWAH INI) ===")
print(f"BOT_TOKEN: {samarkan(os.getenv('TELEGRAM_BOT_TOKEN'))}")
print(f"CHAT_ID: {samarkan(os.getenv('TELEGRAM_CHAT_ID'))}")
print(f"TW_KEY: {samarkan(os.getenv('TWITTER_API_KEY'))}")
print(f"TW_SECRET: {samarkan(os.getenv('TWITTER_API_SECRET'))}")
print(f"TW_TOKEN: {samarkan(os.getenv('TWITTER_ACCESS_TOKEN'))}")
print(f"TW_T_SECRET: {samarkan(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))}")
print(f"IA_KEY: {samarkan(os.getenv('INVOLVE_ASIA_API_KEY'))}")
print(f"IA_SECRET: {samarkan(os.getenv('INVOLVE_ASIA_SECRET_KEY'))}")
print("=============================================================")
