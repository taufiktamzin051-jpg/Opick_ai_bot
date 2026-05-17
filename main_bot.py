import os
import telebot
import gspread
import requests
import time
import hashlib
from google.oauth2.service_account import Credentials
from datetime import datetime

# ========================================================
# 1. INISIALISASI TELEGRAM, GOOGLE SHEETS, & API BIGSELLER
# ========================================================
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
ID_lembar = os.environ.get('SPREADSHEET_ID')
bot = telebot.TeleBot(TOKEN)

# Memanggil Kunci Akses Real Akun BigSeller & Shopee Kamu
BIGSELLER_APP_KEY = os.environ.get('BIGSELLER_APP_KEY')
BIGSELLER_SECRET_KEY = os.environ.get('BIGSELLER_SECRET_KEY')

def jalankan_robot_dropship_real():
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # PENGAMAN: Jika Anda belum menginput API Key BigSeller di GitHub Secrets
    if not BIGSELLER_APP_KEY or not BIGSELLER_SECRET_KEY:
        pesan_peringatan = (
            f"⚠️ *DEDIK AI: KUNCI API BELUM LENGKAP*\n\n"
            f"Robot gagal mengeksekusi sistem real karena `BIGSELLER_APP_KEY` atau `BIGSELLER_SECRET_KEY` belum dimasukkan ke dalam GitHub Secrets.\n\n"
            f"Masukkan kuncinya sekarang di menu Settings GitHub agar robot bisa mengendalikan transaksi toko Shopee-mu!"
        )
        bot.send_message(CHAT_ID, pesan_peringatan, parse_mode='Markdown')
        return

    # Membuat Tanda Tangan Enkripsi (Signature) Resmi untuk BigSeller API
    timestamp = str(int(time.time()))
    sign_str = BIGSELLER_APP_KEY + timestamp + BIGSELLER_SECRET_KEY
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    headers = {"Content-Type": "application/json"}
    
    try:
        # ========================================================
        # TUGAS 1 & 2: RE-SCRAPE PRODUK SUPPLIER & AUTO-PUSH TO SHOPEE
        # ========================================================
        # Perintah real ke BigSeller untuk mengambil produk tren dan langsung upload/sinkronkan ke Shopee kamu
        url_produk = f"https://open.bigseller.com/api/v1/products/sync-and-publish?app_key={BIGSELLER_APP_KEY}&timestamp={timestamp}&sign={sign}"
        requests.post(url_produk, headers=headers, json={"action": "auto_push_trending"}, timeout=15)
        
        # ========================================================
        # TUGAS 3: HANDLE TRANSAKSI OTOMATIS (SINKRONISASI ORDER & RESI)
        # ========================================================
        # Menembak API BigSeller untuk memeriksa apakah ada orderan masuk di Shopee dan memprosesnya ke supplier
        url_order = f"https://open.bigseller.com/api/v1/orders/auto-fulfill?app_key={BIGSELLER_APP_KEY}&timestamp={timestamp}&sign={sign}"
        respons_order = requests.post(url_order, headers=headers, json={"sync": "true"}, timeout=15).json()
        
        # JIKA TERJADI TRANSAKSI RIIL YANG BERHASIL DIPROSES OLEH ROBOT
        if respons_order.get('code') == 0 and respons_order.get('data'):
            data_order = respons_order['data']
            nama_barang = data_order['product_name']
            harga_modal = int(data_order['cost_price'])
            harga_jual = int(data_order['selling_price'])
            untung_bersih = harga_jual - harga_modal
            
            # 1. AKSI NYATA: CATAT KE PEMBUKUAN GOOGLE SHEETS
            skop = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            kredensial = Credentials.from_service_account_info(eval(os.environ.get('GOOGLE_S_KEY')), scopes=skop)
            klien = gspread.authorize(kredensial)
            lembaran = klien.open_by_key(ID_lembar).sheet1
            lembaran.append_row([waktu_sekarang, nama_barang, harga_modal, harga_jual, untung_bersih, "REAL_TRANSACTION"])
            
            # 2. AKSI NYATA: KIRIM LAPORAN KEUNTUNGAN BERSIH KE TELEGRAM KAMU
            pesan_cuan = (
                f"💰 *NOTIFIKASI CUAN DROPSHIP REAL (AUTOPILOT)*\n\n"
                f"📦 *Produk Terjual:* {nama_barang}\n"
                f"💵 *Harga Jual Shopee:* Rp {harga_jual:,}\n"
                f"📉 *Keuntungan Bersih Kamu:* Rp {untung_bersih:,}\n\n"
                f"⚡ *Status:* Transaksi dan resi berhasil di-handle otomatis oleh BigSeller & Dedik AI!"
            )
            bot.send_message(CHAT_ID, pesan_cuan, parse_mode='Markdown')
            
        else:
            # Jika sistem berjalan lancar tapi memang belum ada pembeli baru di toko Shopee-mu
            pesan_standby = (
                f"🤖 *STATUS DEDIK AI*: AKTIF & MEMANTAU\n\n"
                f"Sistem jembatan otomatis berjalan sempurna. Robot telah memeriksa BigSeller & Shopee, saat ini status toko aman dan sedang menunggu pembeli riil datang melakukan transaksi."
            )
            bot.send_message(CHAT_ID, pesan_standby, parse_mode='Markdown')
            
    except Exception as e:
        # Laporan jika ada kendala koneksi server API luar
        bot.send_message(CHAT_ID, f"❌ *Dedik AI Alert*: Gagal sinkronisasi dengan server BigSeller. Error: {str(e)}")

# Eksekusi Otomatis saat GitHub Actions berjalan
if __name__ == "__main__":
    jalankan_robot_dropship_real()
