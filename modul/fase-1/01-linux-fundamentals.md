# Modul 1.1: Linux & Server Management Fundamentals untuk DevOps

Dokumentasi ini adalah bagian dari **Fase 1: Pondasi Sistem, Scripting & Kontainerisasi** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Mengapa Linux Menjadi Standar DevOps?

Di dunia produksi:
* Lebih dari **95% server cloud** (Google Cloud Platform, AWS, Azure) berjalan di atas distribusi Linux (Ubuntu, Debian, RedHat/CentOS, Alpine).
* **Container Docker** membungkus aplikasi Anda di atas kernel Linux.
* Service hemat biaya seperti **GCP Cloud Run** menjalankan container Linux serverless.

Memahami Linux memungkinkan Anda:
1. Memeriksa performa server saat pemrosesan ETL data lambat.
2. Membaca dan menganalisis log error transaksi penjualan.
3. Menghindari kesalahan izin file (*permission denied*) yang sering menggagalkan proses deployment.

---

## 2. Struktur File Linux vs Windows

Di Windows, drive terpisah seperti `C:\` dan `D:\`. Di Linux, **semua file berakar dari satu direktori tunggal (*root*)**: `/`.

```
/ (Root Directory)
 ├── etc/         --> Konfigurasi sistem & aplikasi (NGINX, database, environment variables)
 ├── var/log/     --> Log aplikasi & sistem (krusial untuk monitoring & troubleshoot)
 ├── home/        --> Folder pribadi user biasa (contoh: /home/tbsuser)
 ├── tmp/         --> File sementara (buffer download/export file data penjualan)
 ├── opt/         --> Lokasi standar instalasi aplikasi custom pihak ketiga
 └── bin/ & sbin/ --> Perintah/executable biner sistem (ls, grep, cat, dll.)
```

---

## 3. Perintah Esensial DevOps Berdasarkan Kategori

### A. Navigasi & File
| Perintah | Deskripsi | Contoh Kasus Nyata |
| :--- | :--- | :--- |
| `pwd` | Print Working Directory (cek lokasi saat ini) | Memastikan posisi direktori sebelum menjalankan script |
| `ls -lah` | List file lengkap (termasuk file `.env`, ukuran manusiawi) | Mengecek apakah file config tersembunyi sudah ada |
| `mkdir -p a/b/c` | Buat folder bertingkat sekaligus jika belum ada | Membuat direktori `logs/penjualan/backup/` |
| `cp -r src/ dest/`| Salin folder beserta seluruh isinya | Backup folder konfigurasi sebelum diubah |
| `rm -rf tmp_dir` | Hapus direktori beserta isinya secara rekursif | Bersihkan cache data build (gunakan hati-hati!) |

### B. Inspeksi & Manipulasi Data Log (Sangat Penting untuk Data & Support)
| Perintah | Deskripsi | Contoh Kasus Nyata |
| :--- | :--- | :--- |
| `head -n 20 file.csv` | Tampilkan 20 baris pertama | Cek struktur header file data penjualan |
| `tail -n 50 app.log` | Tampilkan 50 baris terakhir | Cek error terbaru yang baru saja terjadi |
| `tail -f app.log` | Monitor log secara *live / streaming* | Pantau status saat cron ETL sedang berjalan |
| `grep -i "error" app.log` | Cari kata kunci "error" (case-insensitive) | Filter hanya baris error dari ribuan transaksi |
| `grep -C 3 "FAIL" app.log` | Cari kata "FAIL" + 3 baris sebelum & sesudahnya | Mengetahui konteks penyebab kegagalan transaksi |
| `wc -l data.csv` | Hitung jumlah baris file secara instan | Validasi apakah jumlah record penjualan sesuai ekspektasi |

### C. Permissions (Hak Akses)
Setiap file di Linux memiliki atribut hak akses untuk 3 pihak:
1. **User (Owner):** Pemilik file
2. **Group:** Anggota grup pemilik
3. **Others:** Semua orang / publik

Nilai angka hak akses:
* **Read (r) = 4**
* **Write (w) = 2**
* **Execute (x) = 1**

```
Contoh Permission: -rwxr-xr--
- rwx  (Owner) : 4 + 2 + 1 = 7  (Bisa baca, tulis, eksekusi)
- r-x  (Group) : 4 + 0 + 1 = 5  (Bisa baca, eksekusi)
- r--  (Others): 4 + 0 + 0 = 4  (Hanya bisa baca)
Total permission: 754
```

Perintah pengubah hak akses:
* `chmod +x script.sh` : Memberikan hak eksekusi ke script.
* `chmod 600 id_rsa` : Mengunci file credential/SSH key hanya untuk owner (wajib untuk keamanan cloud).
* `chown tbsuser:tbsgroup app.py` : Mengubah user & grup pemilik file.

### D. Monitoring Resource & Proses
| Perintah | Deskripsi | Kapan Digunakan |
| :--- | :--- | :--- |
| `ps aux \| grep python` | Cari proses Python yang sedang berjalan | Memastikan proses ETL berjalan di background |
| `top` atau `htop` | Task manager versi terminal | Mengecek proses yang memakan CPU/RAM 100% |
| `kill -9 <PID>` | Hentikan paksa proses berdasarkan PID | Mematikan script yang macet/infinite loop |
| `df -h` | Cek kapasitas disk storage server | Deteksi disk penuh akibat log menumpuk |
| `free -m` | Cek sisa memori RAM (dalam Megabyte) | Deteksi *out-of-memory* (OOM) |

---

## 4. Mini Lab Mandiri: Simulasi Troubleshooting Log Penjualan

Di folder `labs/fase-1/`, sudah disiapkan file simulasi `sales_transactions.log` untuk latihan langsung.

### Latihan Praktik:
1. **Cek Ukuran & Baris Data:**
   Hitung berapa total baris log transaksi:
   ```bash
   wc -l labs/fase-1/sales_transactions.log
   ```

2. **Cari Error Transaksi:**
   Tampilkan semua transaksi yang gagal/error:
   ```bash
   grep -i "error" labs/fase-1/sales_transactions.log
   ```

3. **Hitung Jumlah Error:**
   Gunakan kombinasi pipe (`|`) untuk menghitung berapa kali kata `ERROR` muncul:
   ```bash
   grep -i "error" labs/fase-1/sales_transactions.log | wc -l
   ```

4. **Ambil 10 Error Terakhir:**
   ```bash
   grep -i "error" labs/fase-1/sales_transactions.log | tail -n 10
   ```

