# Modul 1.3: Docker & Containerization Fundamentals

Dokumentasi ini adalah bagian dari **Fase 1: Pondasi Sistem, Scripting & Kontainerisasi** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Masalah Klasik: "Di Laptop Saya Jalan, Pas di Server Kok Error?"

Sebelum ada Docker, skenario ini terjadi setiap hari:
* Developer mengembangkan aplikasi dashboard dengan Python 3.11 dan library Pandas versi 2.0 di laptop Windows.
* Ketika di-deploy ke server kantor (Ubuntu Linux), server ternyata terpasang Python 3.8 versi lawas, dan dependency gagal ter-install karena ada pustaka C/C++ yang hilang di OS.
* **Hasilnya:** Aplikasi crash di server produksi dan saling menyalahkan antara tim developer dan tim sysadmin.

**Solusi Docker:**
Docker membungkus seluruh aplikasi Anda bersama dengan:
* Sistem operasi mini (biasanya Linux Alpine atau Debian Slim),
* Runtime bahasa pemrograman (Python, Node.js, dsb.),
* Semua dependensi library (`requirements.txt`),
* File konfigurasi dan kode sumber,

ke dalam satu paket terisolasi yang disebut **Container**. Jika aplikasi berjalan di laptop Anda di dalam container, ia **dijamin 100% berjalan identik di server mana pun** (laptop tim lain, GCP Cloud Run, AWS EC2, atau Kubernetes).

---

## 2. Container vs Virtual Machine (VM)

Apa bedanya Docker dengan Virtual Machine (seperti VirtualBox atau VMware)?

```
   VIRTUAL MACHINE (VM)                  DOCKER CONTAINER
┌─────────────────────────┐          ┌─────────────────────────┐
│ App A    │ App B        │          │ App A    │ App B        │
├──────────┼──────────────┤          ├──────────┼──────────────┤
│ Bins/Libs│ Bins/Libs    │          │ Bins/Libs│ Bins/Libs    │
├──────────┼──────────────┤          ├─────────────────────────┤
│ Guest OS │ Guest OS     │ (Berat!) │     DOCKER ENGINE       │ (Ringan!)
│ (Windows)│ (Ubuntu 2GB) │          ├─────────────────────────┤
├─────────────────────────┤          │     HOST OS KERNEL      │ (Dipakai bersama)
│       HYPERVISOR        │          ├─────────────────────────┤
├─────────────────────────┤          │     HARDWARE FISIK      │
│     HARDWARE FISIK      │          └─────────────────────────┘
└─────────────────────────┘
```

* **Virtual Machine:** Membawa seluruh sistem operasi tiruan (*Guest OS*) lengkap dengan kernel sendiri. Ukuran gigabyte, booting butuh hitungan menit, boros RAM.
* **Container:** Menumpang dan berbagi kernel OS milik *Host*. Ukurannya hanya megabyte, booting instan dalam **hitungan milidetik**, sangat efisien.

---

## 3. Tiga Konsep Kunci Docker

1. **`Dockerfile` (Resep Masakan):**  
   File teks berisi instruksi langkah demi langkah cara membangun lingkungan aplikasi Anda.
2. **`Docker Image` (Kue Matang / Blueprint Beku):**  
   Hasil kompilasi dari Dockerfile. Sifatnya *immutable* (tidak bisa diubah). Blueprint ini bisa disimpan di registry cloud (Google Artifact Registry, Docker Hub).
3. **`Docker Container` (Kue yang Sedang Dimakan / Proses Hidup):**  
   Instance aktif yang berjalan dari Docker Image. Anda bisa menjalankan 10 container sekaligus dari 1 image yang sama.

---

## 4. Anatomi Dockerfile Standar Produksi

Berikut contoh Dockerfile untuk aplikasi dashboard / API data penjualan:

```dockerfile
# 1. Base Image: Gunakan versi slim agar ukuran image kecil (<150MB)
FROM python:3.11-slim

# 2. Set Working Directory di dalam container
WORKDIR /app

# 3. Mencegah Python membuat file .pyc & mengalirkan log langsung ke terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. Copy dependency file terlebih dahulu (memanfaatkan Docker Layer Caching)
COPY requirements.txt .

# 5. Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy seluruh source code aplikasi ke dalam container
COPY . .

# 7. Dokumentasikan port yang digunakan oleh aplikasi
EXPOSE 8080

# 8. Perintah utama yang dijalankan saat container menyala
CMD ["python", "app.py"]
```

> [!TIP]
> **Mengapa COPY requirements.txt dipisah sebelum COPY . . ?**
> Docker menggunakan sistem **Layer Caching**. Jika Anda hanya mengubah 1 baris kode di `app.py` tanpa menambah library baru, Docker tidak akan mengulang proses `pip install`. Proses build akan selesai dalam **1 detik**!

---

## 5. Perintah Wajib Docker (CLI Cheat Sheet)

| Perintah | Fungsi | Contoh |
| :--- | :--- | :--- |
| `docker build` | Membangun image dari Dockerfile | `docker build -t sales-dashboard:v1 .` |
| `docker run` | Menjalankan container baru dari image | `docker run -d -p 8080:8080 --name my-dashboard sales-dashboard:v1` |
| `docker ps` | Melihat daftar container yang sedang aktif | `docker ps` |
| `docker logs` | Membaca log output yang dicetak container | `docker logs -f my-dashboard` |
| `docker exec` | Masuk ke dalam terminal container yang sedang hidup | `docker exec -it my-dashboard sh` |
| `docker stop` | Menghentikan container yang sedang jalan | `docker stop my-dashboard` |
| `docker rm` | Menghapus container yang sudah mati | `docker rm my-dashboard` |

*Catatan Flag `docker run -d -p 8080:8080`:*
* `-d` (*detached*): Menjalankan container di background agar terminal tidak terkunci.
* `-p 8080:8080` (*port forwarding*): Meneruskan traffic dari `localhost:8080` laptop Anda ke port `8080` di dalam container.

---

## 6. Mini Lab Mandiri: Menjalankan Aplikasi Penjualan Pertama di Docker

Di folder `labs/fase-1/sample-app/`, sudah disiapkan aplikasi web mini Python (`app.py`) yang menampilkan ringkasan data penjualan TBS Food beserta `Dockerfile`-nya.

Langkah prakteknya:
1. Pastikan aplikasi **Docker Desktop** di Windows Anda sudah aktif (status: *Engine running*).
2. Ikuti instruksi pada lab di bawah ini untuk mem-build dan menjalankannya!
