from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.stock_service import get_stock_data
from services.ai_service import get_ai_analysis, chat_with_ai

app = FastAPI(title="AI Chatbot Saham API")

# Membuat struktur data untuk menerima pesan Chat
class ChatRequest(BaseModel):
    pesan: str

@app.get("/")
def read_root():
    # Mengembalikan file HTML ke browser, bukan lagi teks JSON
    return FileResponse("frontend/index.html")

@app.get("/api/saham/{ticker}")
def cek_saham(ticker: str):
    return get_stock_data(ticker)

@app.get("/api/analisis/{ticker}")
def analisis_saham(ticker: str):
    data_saham = get_stock_data(ticker)
    if "error" in data_saham:
        return {"status": "gagal", "pesan": data_saham["error"]}
        
    analisis_ai = get_ai_analysis(data_saham)
    return {
        "status": "sukses",
        "data_saham": data_saham,
        "analisis_ai": analisis_ai
    }

# --- ENDPOINT BARU KHUSUS CHATBOT (POST) ---
@app.post("/api/chat")
def chatbot_endpoint(request: ChatRequest):
    # Mengirim pesan pengguna ke otak Gemini
    jawaban_ai = chat_with_ai(request.pesan)
    
    return {
        "status": "sukses",
        "pesan_pengguna": request.pesan,
        "jawaban_ai": jawaban_ai
    }