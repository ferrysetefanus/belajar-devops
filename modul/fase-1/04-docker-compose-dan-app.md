# Modul 1.4: Multi-Container Orchestration dengan Docker Compose

Dokumentasi ini adalah bagian penutup dari **Fase 1: Pondasi Sistem, Scripting & Kontainerisasi** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Mengapa Perlu Docker Compose?

Pada Modul 1.3, Anda berhasil menjalankan 1 container tunggal. Namun di dunia nyata, sistem kantor tidak pernah sesederhana itu:
* Ada **Web Dashboard / API** (Python).
* Ada **Database** (PostgreSQL / MySQL) untuk menyimpan transaksi penjualan.
* Ada **Worker ETL** yang bertugas menyedot data penjualan harian ke database.

Jika Anda menggunakan `docker run` biasa:
1. Anda harus mengetik perintah terminal yang panjang berkali-kali.
2. **Masalah Networking:** Bagaimana container Dashboard memanggil database? IP address container selalu berubah-ubah setiap kali restart.
3. **Masalah Kehilangan Data (Data Persistence):** Secara default, jika container database dimatikan/dihapus, **seluruh data penjualan di dalamnya ikut lenyap!**

**Solusi:**  
**Docker Compose** memungkinkan Anda mendefinisikan seluruh arsitektur multi-container, jaringan komunikasi internal (*networking*), dan penyimpanan permanen (*volumes*) dalam satu file deklaratif: `docker-compose.yml`.

Cukup satu perintah:
```bash
docker compose up -d
```
Seluruh ekosistem aplikasi langsung menyala secara otomatis, terhubung satu sama lain, dan aman.

---

## 2. Tiga Konsep Fundamental Docker Compose

### A. Service Discovery & Docker Internal DNS
Di dalam jaringan Docker Compose, container tidak perlu tahu IP address rekannya. Docker menyediakan **DNS internal otomatis berdasarkan nama service**:
* Jika service database Anda beri nama `db`, maka aplikasi Python Anda cukup terhubung ke host: **`db:5432`**.

### B. Persistent Storage (Docker Volumes)
Container bersifat *ephemeral* (sementara). Agar data tabel penjualan tidak hilang saat container PostgreSQL di-restart atau di-upgrade, kita wajib memasang **Volume**:
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```
Data fisik akan disimpan dengan aman di harddisk laptop/server Anda, terpisah dari siklus hidup container.

### C. Dependency & Startup Order (`depends_on`)
Aplikasi Dashboard tidak boleh menyala sebelum Database siap menerima koneksi. Kita mengatur urutan startup menggunakan perintah `depends_on`.

---

## 3. Anatomi File `docker-compose.yml`

Berikut contoh arsitektur nyata untuk TBS Food:

```yaml
version: '3.8'

services:
  # 1. Service Database PostgreSQL
  db:
    image: postgres:16-alpine
    container_name: tbs-postgres
    restart: always
    environment:
      POSTGRES_USER: tbs_admin
      POSTGRES_PASSWORD: SecretPassword123
      POSTGRES_DB: tbs_sales_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # 2. Service Dashboard Web Penjualan
  dashboard:
    build:
      context: ./sample-app
      dockerfile: Dockerfile
    container_name: tbs-sales-dashboard
    restart: always
    ports:
      - "8080:8080"
    environment:
      PORT: 8080
      DB_HOST: db        # Memanggil nama service 'db' di atas!
      DB_PORT: 5432
      DB_NAME: tbs_sales_db
      DB_USER: tbs_admin
      DB_PASSWORD: SecretPassword123
    depends_on:
      - db

# 3. Definisi Volume Permanen
volumes:
  postgres_data:
```

---

## 4. Perintah Wajib Docker Compose (Cheat Sheet)

| Perintah | Deskripsi |
| :--- | :--- |
| `docker compose up -d` | Build dan jalankan seluruh container di background |
| `docker compose ps` | Lihat status seluruh container dalam compose |
| `docker compose logs -f` | Streaming log seluruh service sekaligus |
| `docker compose logs -f dashboard` | Streaming log hanya untuk service dashboard |
| `docker compose restart <service>` | Restart salah satu service tanpa mematikan yang lain |
| `docker compose down` | Hentikan dan bersihkan container (data volume tetap aman!) |
| `docker compose down -v` | Hentikan container DAN hapus seluruh data volume (reset bersih) |

---

## 5. Mini Lab Mandiri: Menjalankan Ekosistem Dashboard + PostgreSQL

File `docker-compose.yml` sudah disiapkan di folder:  
👉 [`labs/fase-1/docker-compose.yml`](../../labs/fase-1/docker-compose.yml)

Ikuti langkah uji coba pada panduan di bawah untuk melihat keajaiban integrasi multi-container!

