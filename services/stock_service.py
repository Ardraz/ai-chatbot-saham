from datetime import datetime
import random

def get_stock_data(ticker_symbol):
    # Memastikan saham Indonesia menggunakan akhiran .JK
    if not ticker_symbol.upper().endswith(".JK"):
        ticker_symbol = f"{ticker_symbol.upper()}.JK"
        
    # Memastikan format tanggal secara ketat DD/MM/YYYY
    tanggal_sekarang = datetime.now().strftime("%d/%m/%Y")
    
    # --- MOCK DATA (Data Simulasi) ---
    # -------------------------------------------------------------------------
    # PENTING (CATATAN DEVELOPER): 
    # Karena saat ini berjalan di Cloud IDE (Codespaces), IP sering diblokir 
    # oleh penyedia data finansial. Oleh karena itu, digunakan MOCK DATA.
    # Jika di-deploy di server berbayar atau localhost, silakan ganti blok 
    # ini dengan pemanggilan API yfinance langsung.
    # -------------------------------------------------------------------------
    # Database tiruan ini menjaga agar pengembangan AI tidak terhenti oleh blokir server API eksternal
    mock_db = {
        "BBCA.JK": {"nama": "Bank Central Asia Tbk", "harga": 9800, "per": 22.5, "pbv": 4.8},
        "BBRI.JK": {"nama": "Bank Rakyat Indonesia Tbk", "harga": 6200, "per": 15.2, "pbv": 2.9},
        "ANTM.JK": {"nama": "Aneka Tambang Tbk", "harga": 1550, "per": 12.1, "pbv": 1.5},
        "TLKM.JK": {"nama": "Telkom Indonesia Tbk", "harga": 3100, "per": 14.3, "pbv": 2.1}
    }
    
    # Jika emiten ada di database tiruan, gunakan data tersebut. Jika tidak, buat angka acak realistis.
    data = mock_db.get(ticker_symbol, {
        "nama": ticker_symbol,
        "harga": random.randint(1000, 10000),
        "per": round(random.uniform(10.0, 25.0), 2),
        "pbv": round(random.uniform(1.0, 5.0), 2)
    })
    
    return {
        "tanggal": tanggal_sekarang,
        "simbol": ticker_symbol,
        "nama_perusahaan": data["nama"],
        "harga_saat_ini": data["harga"],
        "per_ratio": data["per"],
        "pbv_ratio": data["pbv"],
        "catatan": "Menggunakan Data Simulasi (Mock) karena IP Server diblokir"
    }