# Modul 2.3: Serverless Deployment ke Google Cloud Run

Dokumentasi ini adalah bagian dari **Fase 2: Implementasi GCP Hemat Biaya & CI/CD Pipeline** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Konsep Stateless vs Stateful (Prinsip Emas Cloud Run)

Sebelum mendeploy, mari kita kunci satu prinsip arsitektur yang sangat penting:

* **Cloud Run = STATELESS (Otak Pemroses):**  
  Aplikasi yang dijalankan di Cloud Run tidak boleh mengandalkan harddisk lokal untuk menyimpan data jangka panjang. Jika container tidur atau di-restart, disk lokalnya akan direset. Cloud Run sangat cocok untuk: **Web Dashboard, Backend API, dan Script ETL**.
* **Database = STATEFUL (Tempat Simpan Data):**  
  Data penjualan harus disimpan di tempat yang memiliki *Persistent Disk* permanen (seperti VM `e2-micro` atau managed database), lalu diakses oleh Cloud Run via koneksi jaringan.

---

## 2. Mengapa Cloud Run Sangat Disukai untuk Dashboard Kantor?

1. **Gratis Alamat HTTPS Resmi:**  
   Google otomatis memberikan URL dengan sertifikat SSL resmi (misal: `https://sales-dashboard-xyz-as.a.run.app`) tanpa perlu beli domain atau setting NGINX/Certbot.
2. **Hemat Biaya Maksimal (*Scale to Zero*):**  
   Dengan parameter `--min-instances=0`, jika tidak ada orang di kantor yang membuka dashboard, container akan tidur dan biayanya **Rp 0**.
3. **Auto-Restart Otomatis:**  
   Jika aplikasi mengalami error atau crash, Google akan otomatis melahirkan container baru dalam hitungan milidetik.

---

## 3. Parameter Penting Perintah `gcloud run deploy`

| Parameter | Fungsi | Rekomendasi TBS Food |
| :--- | :--- | :--- |
| `--image` | Alamat image Docker di Artifact Registry | `asia-southeast2-docker.pkg.dev/the-byway-487902-m9/tbs-repo/sales-dashboard:v1` |
| `--region` | Lokasi server fisik Google | `asia-southeast2` (Jakarta) agar akses cepat |
| `--port` | Port aplikasi di dalam container | `8080` (sesuai setting `EXPOSE` di Dockerfile) |
| `--memory` | Batas RAM per container | `256Mi` (cukup & hemat untuk dashboard internal) |
| `--min-instances` | Jumlah server minimum saat sepi | `0` (wajib 0 agar scale-to-zero / hemat) |
| `--max-instances` | Batas maksimum server jika diserbu traffic | `2` atau `3` (mencegah lonjakan biaya tak terduga) |
| `--allow-unauthenticated` | Apakah web bisa dibuka publik tanpa login GCP | Dicentang/diizinkan agar tim kantor bisa akses |

---

## 4. Langkah Praktik Deployment ke Cloud Run

Jalankan perintah ini di terminal **Google Cloud Shell**:

```bash
gcloud run deploy tbs-sales-dashboard \
    --image=asia-southeast2-docker.pkg.dev/the-byway-487902-m9/tbs-repo/sales-dashboard:v1 \
    --region=asia-southeast2 \
    --platform=managed \
    --allow-unauthenticated \
    --port=8080 \
    --memory=256Mi \
    --min-instances=0 \
    --max-instances=2
```

### Apa yang Terjadi Saat Perintah Dijalankan?
1. Google Cloud Run akan menarik image `sales-dashboard:v1` dari Artifact Registry Anda di Jakarta.
2. Google menyiapkan infrastruktur serverless, konfigurasi routing, dan sertifikat HTTPS.
3. Di akhir proses, terminal akan menampilkan pesan:
   ```
   Service [tbs-sales-dashboard] revision [...] has been deployed and is serving 100 percent of traffic.
   Service URL: https://tbs-sales-dashboard-xxxxx-as.a.run.app
   ```
4. Salin **Service URL** tersebut dan buka di browser handphone atau laptop Anda. Aplikasi penjualan TBS Food Anda sekarang resmi live di internet!

