import os
import requests
import time
import hashlib
from datetime import datetime

def jalankan_dropship_autopilot():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ambil Kunci Rahasia dari GitHub Secrets
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    BIGSELLER_APP_KEY = os.environ.get('BIGSELLER_APP_KEY')
    BIGSELLER_SECRET_KEY = os.environ.get('BIGSELLER_SECRET_KEY')
    
    if not BIGSELLER_APP_KEY or not BIGSELLER_SECRET_KEY:
        print("API BigSeller belum diisi di GitHub Secrets!")
        return

    # Membuat Kunci Enkripsi Masuk ke Server BigSeller
    timestamp = str(int(time.time()))
    sign_str = BIGSELLER_APP_KEY + timestamp + BIGSELLER_SECRET_KEY
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    headers = {"Content-Type": "application/json"}
    
    try:
        # 🔄 TUGAS 1 & 2: Ambil Produk Supplier & Lempar Otomatis ke Shopee kamu
        url_produk = f"https://open.bigseller.com/api/v1/products/sync-and-publish?app_key={BIGSELLER_APP_KEY}&timestamp={timestamp}&sign={sign}"
        requests.post(url_produk, headers=headers, json={"action": "auto_push_trending"}, timeout=15)
        
        # 🛒 TUGAS 3: Cek Orderan Masuk Shopee & Perintahkan BigSeller Transaksi Otomatis ke Supplier
        url_order = f"https://open.bigseller.com/api/v1/orders/auto-fulfill?app_key={BIGSELLER_APP_KEY}&timestamp={timestamp}&sign={sign}"
        respons = requests.post(url_order, headers=headers, json={"sync": "true"}, timeout=15).json()
        
        # SIAPKAN NOTIFIKASI TELEGRAM
        url_tele = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        
        if respons.get('code') == 0 and respons.get('data'):
            data_order = respons['data']
            untung_bersih = int(data_order['selling_price']) - int(data_order['cost_price'])
            
            pesan = (
                f"💰 *CUAN DROPSHIP REAL MASUK!*\n\n"
                f"📦 *Produk:* {data_order['product_name']}\n"
                f"📈 *Untung Bersih:* Rp {untung_bersih:,}\n"
                f"⚡ *Status:* Sukses di-handle Autopilot BigSeller ⇄ Shopee!"
            )
        else:
            pesan = f"🤖 *Dedik AI Status:* Sistem Real Aktif Memantau. Jam {waktu} belum ada orderan baru masuk di Shopee. Robot stand-by mendengarkan pasar!"
            
        requests.post(url_tele, data={"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"})
        print("Eksekusi sukses!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    jalankan_dropship_autopilot()
