# Menggunakan mesin Python versi ringan
FROM python:3.9-slim

# Menentukan folder kerja di dalam server
WORKDIR /app

# Memasukkan file daftar pustaka
COPY requirements.txt .

# Menginstal pustaka yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Memasukkan seluruh file kode Anda ke dalam server
COPY . .

# Hugging Face secara otomatis membuka Port 7860, jadi kita jalankan FastAPI di port tersebut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]