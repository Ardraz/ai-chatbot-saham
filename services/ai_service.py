import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Membuka "Brankas"
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_analysis(stock_data):
    # --- AUTO-DISCOVERY MODEL ---
    model_name_to_use = None
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name_to_use = m.name
                if 'flash' in m.name.lower():
                    break
    except Exception as e:
        return f"Gagal mengecek daftar model: {str(e)}"
        
    if not model_name_to_use:
        return "Maaf, tidak ada model yang tersedia."

    # --- KONFIGURASI PARAMETER (PENTING UNTUK FINANSIAL) ---
    config = genai.types.GenerationConfig(
        temperature=0.2,          # Suhu rendah agar AI objektif dan tidak berhalusinasi
        top_p=0.8,                # Mengontrol probabilitas kata yang dipilih
        top_k=40,                 # Mengontrol variasi kosakata
        
    )

    # Mengaktifkan model dengan konfigurasi yang sudah dibuat
    model = genai.GenerativeModel(
        model_name=model_name_to_use,
        generation_config=config
    )
    
    # --- PROMPT ENGINEERING: SYSTEM PROMPT ---
    system_prompt = """
    [ATURAN SISTEM]
    Anda adalah seorang analis saham profesional yang objektif. 
    Tugas Anda adalah memberikan analisis fundamental singkat.
    Penting: Jangan pernah memberikan saran investasi atau rekomendasi beli/jual secara eksplisit.
    Gunakan gaya bahasa semi-formal.
    """
    
    # --- PROMPT ENGINEERING: USER PROMPT ---
    user_prompt = f"""
    [DATA SAHAM SAAT INI]
    - Simbol: {stock_data['simbol']}
    - Nama Perusahaan: {stock_data['nama_perusahaan']}
    - Harga Terakhir: Rp {stock_data['harga_saat_ini']}
    - PER (Price to Earning Ratio): {stock_data['per_ratio']}
    - PBV (Price to Book Value): {stock_data['pbv_ratio']}
    - Tanggal Data: {stock_data['tanggal']}
    
    Tolong jelaskan secara singkat (maksimal 2 paragraf) apa arti angka PER dan PBV tersebut untuk emiten ini, dan bagaimana kondisi valuasinya secara umum.
    """
    
    # Menggabungkan kedua prompt menjadi satu kesatuan
    final_prompt = system_prompt + "\n" + user_prompt

    try:
        # Mengirim prompt ke server
        response = model.generate_content(final_prompt)
        return f"[Model: {model_name_to_use} | Temp: 0.2]\n\n{response.text}"
    except Exception as e:
        return f"Maaf, AI gagal memproses analisis: {str(e)}"

    # ... (kode get_ai_analysis sebelumnya biarkan saja di atas) ...

def chat_with_ai(user_message):
    model_name_to_use = None
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name_to_use = m.name
                if 'flash' in m.name.lower():
                    break
    except Exception:
        pass
        
    if not model_name_to_use:
        return "Sistem AI sedang tidak tersedia."

    config = genai.types.GenerationConfig(
        temperature=0.3, # Sedikit lebih tinggi dari 0.2 agar bisa lebih luwes mengobrol
        top_p=0.8,
        top_k=40
    )

    model = genai.GenerativeModel(
        model_name=model_name_to_use,
        generation_config=config
    )
    
    # SYSTEM PROMPT KHUSUS CHATBOT
    system_prompt = """
    Anda adalah Asisten AI Analisis Saham Indonesia.
    Gaya bahasa: Semi-Formal, profesional, dan objektif.
    Tugas: Menjawab pertanyaan seputar saham Indonesia.
    Penting: 
    1. Anda tidak boleh memberikan rekomendasi beli/jual saham.
    2. Jika pengguna menanyakan data saham, gunakan pengetahuan umum Anda terkait pasar modal Indonesia.
    """
    
    final_prompt = system_prompt + "\n\nPertanyaan Pengguna: " + user_message

    try:
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        return f"Gagal memproses pesan: {str(e)}"