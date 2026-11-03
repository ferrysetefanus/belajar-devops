# Direktori Pembelajaran DevOps

Selamat datang di repositori materi dan hands-on lab DevOps personal. Seluruh modul, catatan teori, script latihan, dan implementasi riil disimpan secara terstruktur di sini agar Anda dan AI agent dapat melanjutkan proses pembelajaran kapan saja.

---

## 📌 Dokumen Utama
* 🗺️ **[ROADMAP.md](ROADMAP.md)** : Rencana belajar 4 fase (timeline 3–4 bulan, target arsitektur GCP hemat biaya & AWS bridge).
* 📋 **[kurikulum.md](kurikulum.md)** : Kurikulum referensi lengkap dari kursus DevOps Udemy.

---

## 📚 Struktur Modul Pembelajaran

```
DEVOPS/
├── ROADMAP.md
├── kurikulum.md
├── modul/
│   ├── fase-1/
│   │   ├── 01-linux-fundamentals.md        # Modul 1.1: Perintah Linux, Hak Akses & Troubleshooting Log
│   │   ├── 02-bash-scripting.md             # (Next) Modul 1.2: Otomasi Scripting Data & Backup
│   │   ├── 03-docker-dasar.md               # Modul 1.3: Containerization & Dockerfile
│   │   └── 04-docker-compose-dan-app.md     # Modul 1.4: Multi-container Dashboard & DB
│   ├── fase-2/                              # GCP & CI/CD Pipeline (Cloud Run, GitHub Actions)
│   ├── fase-3/                              # Infrastructure as Code (Terraform) & Observability
│   └── fase-4/                              # AWS Bridge & Advanced (Minikube, K8s, GitOps)
└── labs/
    └── fase-1/
        └── sales_transactions.log           # File log dummy untuk praktek analisis & troubleshooting
```

---

## 🚀 Status Progres Saat Ini

### ✅ FASE 1: Pondasi Sistem, Scripting & Kontainerisasi (SELESAI 100%)
- [x] **Modul 1.1: Linux & Server Management Fundamentals**  
  File: [`modul/fase-1/01-linux-fundamentals.md`](modul/fase-1/01-linux-fundamentals.md) | Lab: [`labs/fase-1/sales_transactions.log`](labs/fase-1/sales_transactions.log)
- [x] **Modul 1.2: Bash Scripting untuk Otomasi Data Penjualan**  
  File: [`modul/fase-1/02-bash-scripting.md`](modul/fase-1/02-bash-scripting.md) | Lab: [`labs/fase-1/backup_and_filter.sh`](labs/fase-1/backup_and_filter.sh)
- [x] **Modul 1.3: Docker Containerization Fundamentals**  
  File: [`modul/fase-1/03-docker-dasar.md`](modul/fase-1/03-docker-dasar.md) | Lab: [`labs/fase-1/sample-app/`](labs/fase-1/sample-app/)
- [x] **Modul 1.4: Multi-Container Docker Compose**  
  File: [`modul/fase-1/04-docker-compose-dan-app.md`](modul/fase-1/04-docker-compose-dan-app.md) | Lab: [`labs/fase-1/docker-compose.yml`](labs/fase-1/docker-compose.yml)

---

### ⏳ FASE 2: Implementasi GCP Hemat Biaya & CI/CD Pipeline
- [x] **Modul 2.1: Fondasi GCP & Navigasi Cloud Console / Cloud Shell**  
  File: [`modul/fase-2/01-gcp-fundamentals-dan-setup.md`](modul/fase-2/01-gcp-fundamentals-dan-setup.md)  
  *Status:* Berhasil setup Project GCP & mengaktifkan API.
- [x] **Modul 2.2: Google Artifact Registry & Image Management di Cloud**  
  File: [`modul/fase-2/02-artifact-registry.md`](modul/fase-2/02-artifact-registry.md)  
  *Status:* Image `sales-dashboard:v1` berhasil di-build dan disimpan di Artifact Registry (region Jakarta).
- [x] **Modul 2.3: Serverless Deployment ke Cloud Run & Scheduled ETL Jobs**  
  File: [`modul/fase-2/03-cloud-run-deployment.md`](modul/fase-2/03-cloud-run-deployment.md)  
  *Status:* Berhasil deploy service `tbs-sales-dashboard` ke Google Cloud Run (HTTPS live di region Jakarta: `asia-southeast2`).
- [x] **Modul 2.4: Otomasi CI/CD dengan GitHub Actions**  
  File: [`modul/fase-2/04-cicd-github-actions.md`](modul/fase-2/04-cicd-github-actions.md)  
  Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)  
  *Status:* Pipeline CI/CD terkonfigurasi & siap dideploy otomatis via `git push`.

# belajar-devops
