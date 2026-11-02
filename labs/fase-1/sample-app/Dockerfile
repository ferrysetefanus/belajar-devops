# Gunakan official python slim image sebagai base
FROM python:3.11-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Atur environment variable agar log langsung keluar ke konsol
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    ENV="Production Docker Container"

# Copy kode aplikasi ke dalam container
COPY app.py .

# Dokumentasikan port yang digunakan
EXPOSE 8080

# Jalankan server
CMD ["python", "app.py"]

