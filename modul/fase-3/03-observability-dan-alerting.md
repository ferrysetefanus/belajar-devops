# Modul 3.3: Observability, Cloud Monitoring & Alerting Otomatis

Dokumentasi ini adalah bagian penutup dari **Fase 3: Infrastructure as Code (IaC) & Observability** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Mengapa Sistem Butuh "Observability"?

Bayangkan skenario buruk di hari Senin pagi:
* Jam 02:00 pagi: Script ETL penjualan gagal berjalan karena koneksi ke database putus.
* Jam 08:30 pagi: Direktur Utama dan Manajer Penjualan membuka dashboard di browser.
* Layar menampilkan angka Rp 0 atau error.
* Direktur menelepon Anda dengan marah: *"Ferry, kenapa data penjualan hari ini tidak ada?!"*

Sebagai DevOps & Data Engineer handal, Anda **tidak boleh menunggu manusia komplain baru tahu sistem sedang rusak**. Sistem harus memiliki **mata, telinga, dan alarm otomatis**:

```
[ETL Job Error Jam 02:01] 
          │
          ▼  Terdeteksi dalam 10 detik oleh Google Cloud Monitoring
[Robot Pengawas (Alert Policy)] 
          │
          ▼  Mengirim sinyal darurat otomatis
[Notifikasi Email / Telegram / Slack Masuk ke HP Anda] 
          │
"🚨 PERINGATAN: Job tbs-sales-etl-job gagal dieksekusi!"
```

Dengan sistem ini, Anda sudah tahu dan bisa memperbaiki masalahnya jauh sebelum tim kantor bangun di pagi hari!

---

## 2. Tiga Pilar Utama Observability

| Pilar | Pertanyaan yang Dijawab | Contoh Nyata di TBS Food | Tool di Cloud |
| :--- | :--- | :--- | :--- |
| **1. Metrics** | *"Apakah ada yang bermasalah?"* | CPU server VM naik ke 95%, atau RAM Cloud Run tersisa 5%. | Google Cloud Monitoring, Prometheus, Grafana |
| **2. Logs** | *"Kenapa masalah itu terjadi?"* | Baris log detail: `Connection timed out to database 34.28.20.49:5432`. | Google Cloud Logging, Loki |
| **3. Traces** | *"Di mana letak kemacetannya?"* | Waktu total request 3 detik: 2.8 detik dihabiskan untuk query SQL. | Google Cloud Trace, OpenTelemetry |

---

## 3. Langkah Praktik 1: Daftarkan Email Anda Sebagai Saluran Siaga (*Notification Channel*)

Agar Google Cloud tahu ke mana harus mengirimkan email darurat jika terjadi insiden:

1. Buka browser ke: [Google Cloud Monitoring Notification Channels](https://console.cloud.google.com/monitoring/alerting/notifications).
2. Gulir ke bawah ke bagian **Email**, lalu klik **Add New**.
3. Masukkan:
   * **Email Address:** Email aktif Anda (email pribadi atau kantor).
   * **Display Name:** `DevOps Alert - Ferry`
4. Klik **Save**.

---

## 4. Langkah Praktik 2: Buat Aturan Alarm (*Log-Based Alert Policy*) via Cloud Shell

Kita akan membuat aturan alarm: **"Jika ada satupun pesan berstatus ERROR pada script ETL data penjualan, kirim sinyal darurat seketika!"**

Buka terminal **Google Cloud Shell** Anda dan jalankan perintah ini:

```bash
# 1. Ambil ID saluran email yang baru Anda buat
CHANNEL_ID=$(gcloud beta monitoring channels list --filter='displayName:"DevOps Alert - Ferry"' --format='value(name)')

# 2. Buat file konfigurasi Alert Policy otomatis
cat << EOF > ~/etl-alert-policy.json
{
  "displayName": "Peringatan Darurat: ETL Penjualan TBS Food Gagal",
  "documentation": {
    "content": "Perhatian Tim DevOps: Script ETL data penjualan mengalami kegagalan pada saat penarikan/transformasi data. Segera periksa log di Cloud Logging!",
    "mimeType": "text/markdown"
  },
  "conditions": [
    {
      "displayName": "Ada Log Error pada Cloud Run Job",
      "conditionMatchedLog": {
        "filter": "resource.type=\"cloud_run_job\" AND severity>=ERROR"
      }
    }
  ],
  "notificationChannels": [
    "$CHANNEL_ID"
  ],
  "alertStrategy": {
    "notificationRateLimit": {
      "period": "300s"
    }
  }
}
EOF

# 3. Aktifkan Alert Policy tersebut di Google Cloud
gcloud alpha monitoring policies create --policy-from-file=~/etl-alert-policy.json
```

---

## 5. Langkah Praktik 3: Simulasi Insiden (Uji Coba Alarm Kebakaran)

Bagaimana membuktikan alarm ini bekerja? Mari kita sengaja memicu sebuah error palsu di terminal Cloud Shell:

```bash
gcloud logging write tbs-sales-etl-job "FATAL ERROR: Database connection failed during batch ETL execution!" --severity=ERROR
```

Dalam waktu **kurang dari 1 menit**, buka aplikasi Gmail / Inbox email Anda:  
Google Cloud Monitoring akan mengirimkan surat resmi berisi:  
**`[FIRING] Peringatan Darurat: ETL Penjualan TBS Food Gagal`**!

Selamat! Sistem Anda kini tidak hanya otomatis berjalan, tetapi juga **otomatis mengawasi dirinya sendiri 24 jam sehari**!
