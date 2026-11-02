# Modul 1.2: Bash Scripting untuk Otomasi DevOps & Data

Dokumentasi ini adalah bagian dari **Fase 1: Pondasi Sistem, Scripting & Kontainerisasi** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Mengapa Bash Scripting Wajib untuk DevOps?

Di dunia produksi, Anda tidak mungkin mengetik perintah terminal satu per satu setiap hari jam 2 pagi untuk:
* Melakukan backup database data penjualan.
* Mengarsip dan membersihkan log yang membengkak agar disk server tidak penuh (*100% disk full*).
* Memeriksa kesehatan service (*health-check*) sebelum proses deployment.

**Bash script** adalah cara kita menyusun kumpulan perintah terminal ke dalam satu file yang dapat dieksekusi secara otomatis oleh sistem (misalnya via *Cron Job* atau *CI/CD Runner*).

---

## 2. Tiga Mantra Emas Bash Script Produksi: `set -euo pipefail`

Secara default, Bash memiliki kelemahan berbahaya: **jika satu baris perintah gagal/error, Bash akan tetap mengeksekusi baris berikutnya sampai selesai**. 

Contoh skenario petaka:
```bash
# Tanpa pengaman:
cd /folder_yang_tidak_ada    # Gagal pindah folder! Tetap di folder sekarang (misal: /)
rm -rf *                     # BENCANA: Menghapus seluruh file di root sistem!
```

Oleh karena itu, setiap script DevOps profesional **wajib** mencantumkan mantra ini di awal file:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

* **`-e` (errexit):** Hentikan script seketika jika ada satu perintah yang menghasilkan error (exit code $\neq$ 0).
* **`-u` (nounset):** Anggap error jika ada variabel yang belum didefinisikan tapi dipanggil (mencegah typo variabel).
* **`-o pipefail`:** Jika menggunakan pipeline (`perintah1 | perintah2`), jika `perintah1` gagal, keseluruhan perintah dianggap gagal.

---

## 3. Komponen Utama Bash Scripting

### A. Variabel & Timestamp Dinamis
Bash tidak menggunakan spasi di sekitar tanda sama dengan `=`.
```bash
NAMA_PROJECT="TBS Food"
BACKUP_DIR="./backups"
# Format tanggal: TAHUNBULANTANGGAL_JAMMENITDETIK (contoh: 20261102_150000)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
NAMA_FILE_BACKUP="sales_backup_${TIMESTAMP}.tar.gz"
```

### B. Argumen Input dari Luar
* `$0` : Nama file script itu sendiri.
* `$1`, `$2` : Argumen pertama dan kedua yang diberikan saat menjalankan script.
* `$#` : Jumlah argumen yang dikirimkan.

Contoh pemanggilan: `./script.sh Jakarta` $\rightarrow$ `$1` bernilai `"Jakarta"`.

### C. Kondisi (If / Else) & Pengecekan File
Di Bash, tanda kurung siku `[ ... ]` membutuhkan spasi di bagian dalam!
```bash
# Cek apakah folder tujuan sudah ada
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Folder backup belum ada, membuat folder: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# Cek apakah file sumber log ada
if [ -f "$LOG_FILE" ]; then
    echo "File log ditemukan, memproses..."
else
    echo "ERROR: File log tidak ditemukan!" >&2
    exit 1   # Keluar dengan kode error (bukan 0)
fi
```

### D. Exit Codes (Status Selesai)
* `exit 0` : Berhasil tanpa masalah (*Success*).
* `exit 1` (atau angka 1–255 lainnya) : Terjadi kegagalan (*Failure*).  
*Penting:* GitHub Actions dan cron mengandalkan nilai *exit code* ini untuk menentukan apakah build lulus atau gagal.

---

## 4. Studi Kasus Riil: Script Otomasi Backup & Filter Error Transaksi

Skenario kantor:
Setiap kali batch transaksi penjualan selesai, Anda ingin membuat script otomatis yang:
1. Memvalidasi bahwa file log transaksi ada.
2. Menyaring semua baris bertanda `[ERROR]` ke file laporan ringkas `incident_report_<TIMESTAMP>.log`.
3. Mengompresi file log mentah ke dalam arsip `.tar.gz` di folder `backups/`.
4. Menampilkan ringkasan status apakah ada insiden atau semua berjalan normal.

File implementasi script ini sudah dibuatkan di:  
👉 [`labs/fase-1/backup_and_filter.sh`](../../labs/fase-1/backup_and_filter.sh)

---

## 5. Cara Menjalankan Script di Terminal

Buka Git Bash di folder `DEVOPS`, lalu jalankan:

```bash
# 1. Berikan hak akses eksekusi ke file script
chmod +x labs/fase-1/backup_and_filter.sh

# 2. Jalankan script-nya
./labs/fase-1/backup_and_filter.sh labs/fase-1/sales_transactions.log

# 3. Cek hasil folder backup yang terbentuk
ls -lah labs/fase-1/backups/
```

