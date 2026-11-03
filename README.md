# Direktori Pembelajaran DevOps

Selamat datang di repositori materi dan hands-on lab DevOps personal. Seluruh modul, catatan teori, script latihan, dan implementasi riil disimpan secara terstruktur di sini agar Anda dan AI agent dapat melanjutkan proses pembelajaran kapan saja.

---

## 📌 Dokumen Utama
* 🗺️ **[ROADMAP.md](ROADMAP.md)** : Rencana belajar 4 fase (timeline 3–4 bulan, target arsitektur GCP hemat biaya & AWS bridge).
* 🧠 **[DEVOPS-FRAMEWORK.md](modul/DEVOPS-FRAMEWORK.md)** : Kerangka berpikir mental model (C-B-R-D & Pohon Keputusan Cloud-Native).
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

### ✅ FASE 2: Implementasi GCP Hemat Biaya & CI/CD Pipeline (SELESAI 100%)
- [x] **Modul 2.1: Fondasi GCP & Navigasi Cloud Console / Cloud Shell**  
  File: [`modul/fase-2/01-gcp-fundamentals-dan-setup.md`](modul/fase-2/01-gcp-fundamentals-dan-setup.md)  
  *Status:* Berhasil setup Project GCP & mengaktifkan API.
- [x] **Modul 2.2: Google Artifact Registry & Image Management di Cloud**  
  File: [`modul/fase-2/02-artifact-registry.md`](modul/fase-2/02-artifact-registry.md)  
  *Status:* Image berhasil di-build dan disimpan di Artifact Registry (region Jakarta).
- [x] **Modul 2.3: Serverless Deployment ke Cloud Run & Scheduled ETL Jobs**  
  File: [`modul/fase-2/03-cloud-run-deployment.md`](modul/fase-2/03-cloud-run-deployment.md)  
  *Status:* Berhasil deploy service `tbs-sales-dashboard` ke Google Cloud Run (HTTPS live di region Jakarta: `asia-southeast2`).
- [x] **Modul 2.4: Otomasi CI/CD dengan GitHub Actions**  
  File: [`modul/fase-2/04-cicd-github-actions.md`](modul/fase-2/04-cicd-github-actions.md)  
  Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)  
  *Status:* Pipeline CI/CD teruji sukses 100%! Push ke GitHub otomatis deploy ke Cloud Run secara live.
- [x] **Modul 2.5: Integrasi Database PostgreSQL di Compute Engine (e2-micro Always Free)**  
  File: [`modul/fase-2/05-database-e2-micro.md`](modul/fase-2/05-database-e2-micro.md)  
  *Status:* Berhasil setup VM e2-micro di US (`us-central1-a`) dengan IP `34.28.20.49` & PostgreSQL terhubung ke Cloud Run.
- [x] **Modul 2.6: Otomasi Scheduled ETL Worker (Cloud Run Jobs + Cloud Scheduler)**  
  File: [`modul/fase-2/06-cloud-run-jobs-scheduler.md`](modul/fase-2/06-cloud-run-jobs-scheduler.md)  
  *Status:* Berhasil membuat Cloud Run Job `tbs-sales-etl-job` & teruji sukses eksekusi batch agregasi data penjualan.

---

### ⏳ FASE 3: Infrastructure as Code (Terraform) & Observability (ONGOING)
- [x] **Modul 3.1: Konsep IaC & Pengenalan Terraform (HashiCorp HCL)**  
  File: [`modul/fase-3/01-terraform-fundamentals.md`](modul/fase-3/01-terraform-fundamentals.md)  
  *Status:* Memahami filosofi IaC, kelemahan ClickOps, dan siklus perintah `init`, `plan`, `apply`, `destroy`.
- [ ] **Modul 3.2: Otomasi Provisioning Resource GCP dengan Terraform (Google Provider)**  
  File: [`modul/fase-3/02-terraform-gcp-provisioning.md`](modul/fase-3/02-terraform-gcp-provisioning.md)  
  Code: [`terraform/`](terraform/)  
  *Status:* Sedang dikerjakan (praktek `terraform init`, `plan`, dan `apply` membuat GCS Bucket di Jakarta).
- [ ] **Modul 3.3: Monitoring, Logging & Alerting Otomatis ke Telegram/Slack**

# belajar-devops
