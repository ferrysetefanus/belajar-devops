# Modul 2.1: Fondasi GCP & Navigasi Cloud Console / Cloud Shell

Dokumentasi ini adalah bagian awal dari **Fase 2: Implementasi GCP Hemat Biaya & CI/CD Pipeline** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Selamat Datang di Dunia Cloud (Google Cloud Platform)

Di Fase 1, Anda telah berhasil membuat aplikasi dan database berjalan di laptop menggunakan Docker. Namun, laptop Anda tidak bisa menyala 24/7 untuk melayani tim kantor.

Sekarang kita akan membawa container tersebut ke **Google Cloud Platform (GCP)** dengan memanfaatkan:
* Akun gratis / kuota *Always Free Tier*.
* Saldo kredit promo **$10/bulan** (dari langganan Google AI Pro).

---

## 2. Konsep Inti Hierarki GCP

Di GCP, semua hal diorganisasi dalam struktur hierarki berikut:

```
[Organization / Akun Google]
       └── [Billing Account] (Tempat kartu kredit / saldo $10 terhubung)
              └── [Project: tbs-food-devops]  <-- Semua service hidup di sini!
                     ├── Cloud Run (Dashboard API)
                     ├── Cloud Run Jobs (ETL Penjualan)
                     ├── Artifact Registry (Tempat simpan Docker Image)
                     └── Cloud Storage (Bucket backup file)
```

> [!IMPORTANT]
> **Aturan Emas GCP:** Semua resource (VM, database, service) **wajib berada di dalam satu Project ID**. Jika suatu saat Anda ingin menghapus seluruh eksperimen tanpa sisa biaya, cukup hapus (*Shut down*) Project ID tersebut!

---

## 3. Strategi Keamanan Biaya: Memasang Budget Alert

Sebelum menyalakan service apa pun, pasang **Budget Alert** agar Anda tidak pernah terkejut dengan tagihan:

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Pada menu navigasi kiri, pilih **Billing** $\rightarrow$ **Budgets & alerts**.
3. Klik **Create Budget**:
   * **Scope:** Pilih Project Anda (misal `tbs-food-prod` atau project aktif Anda).
   * **Amount:** Pilih **Specified amount**, masukkan nominal **$10** (atau Rp 150.000).
   * **Actions / Triggers:** Pasang ambang batas alert di:
     * **50%** ($5) $\rightarrow$ Kirim email pemberitahuan santai.
     * **80%** ($8) $\rightarrow$ Kirim email peringatan.
     * **100%** ($10) $\rightarrow$ Peringatan batas saldo tercapai.
4. Simpan. Sekarang Anda bisa belajar dengan tenang tanpa takut boncos.

---

## 4. Google Cloud Shell: Terminal Super Gratis di Browser

Anda **tidak wajib meng-install Google Cloud SDK (`gcloud`) di laptop** jika tidak ingin memberatkan memori komputer. GCP menyediakan **Google Cloud Shell**:

* Terminal Linux berbasis Debian yang bisa dibuka langsung di browser.
* **Gratis 100%** dengan kuota 50 jam pemakaian/minggu.
* Sudah otomatis terpasang: `gcloud`, `docker`, `git`, `python`, `terraform`, dan storage gratis 5 GB.
* Sudah otomatis terautentikasi dengan akun Google Anda.

### Cara Membuka Cloud Shell:
Klik ikon terminal **`[>_]`** di pojok kanan atas Google Cloud Console:
```
┌──────────────────────────────────────────────────────────────┐
│ Google Cloud     [Search]                     (🔔)  (>_) (👤)│
└──────────────────────────────────────────────────────────────┘
                                                       ↑
                                              Klik ikon ini!
```

---

## 5. Perintah Wajib `gcloud` CLI (Cheat Sheet)

Buka Cloud Shell (atau terminal laptop jika sudah pasang SDK), lalu pahami 5 perintah dasar ini:

| Perintah | Deskripsi |
| :--- | :--- |
| `gcloud auth list` | Menampilkan akun Google yang sedang aktif |
| `gcloud projects list` | Melihat daftar Project ID yang Anda miliki |
| `gcloud config set project <PROJECT_ID>` | Mengunci target project yang sedang dikerjakan |
| `gcloud services list --enabled` | Melihat API/layanan apa saja yang sudah aktif |
| `gcloud services enable run.googleapis.com artifactregistry.googleapis.com` | Mengaktifkan API Cloud Run & Artifact Registry |

---

## 6. Konsep IAM: User Account vs Service Account

Di DevOps, kita mengenal 2 jenis identitas:

1. **User Account (Manusia):**
   * Akun email Anda (`nama@gmail.com`).
   * Digunakan untuk login ke GCP Console melalui browser dengan password dan 2FA.
2. **Service Account (Robot / Mesin):**
   * Akun khusus tanpa password, berbentuk email sistem (contoh: `github-deployer@tbs-project.iam.gserviceaccount.com`).
   * Menggunakan **JSON Key** atau **Workload Identity**.
   * Diberikan hak akses khusus (*least privilege*) agar script CI/CD **GitHub Actions** bisa men-deploy aplikasi secara otomatis tanpa perlu login manual.

---

## 7. Mini Lab: Persiapan Project & Pengaktifan Layanan

Jalankan perintah ini di **Google Cloud Shell** untuk menyiapkan project Anda bagi Fase 2:

```bash
# 1. Pastikan project target sudah aktif
gcloud config set project <MASUKKAN_PROJECT_ID_ANDA>

# 2. Aktifkan service yang dibutuhkan untuk aplikasi TBS Food
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  cloudscheduler.googleapis.com

# 3. Verifikasi bahwa layanan sudah aktif
gcloud services list --enabled | grep -E "run|artifactregistry|cloudscheduler"
```

