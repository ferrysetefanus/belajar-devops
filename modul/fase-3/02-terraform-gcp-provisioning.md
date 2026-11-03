# Modul 3.2: Otomasi Provisioning GCP dengan Terraform

Dokumentasi ini adalah bagian dari **Fase 3: Infrastructure as Code (IaC) & Observability** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Studi Kasus Riil: Tempat Backup Data Penjualan (Cloud Storage Bucket)

Di Modul 1.2, Anda membuat script Bash yang mengompresi log data penjualan ke format `.tar.gz`.  
Namun, jika file `.tar.gz` tersebut hanya disimpan di harddisk lokal server VM, harddisk lama-lama akan penuh.

Solusi industri terbaik:  
Simpan seluruh file backup ke **Google Cloud Storage (GCS Bucket)**.  
Daripada membuat bucket lewat klik-klik di browser (ClickOps), kita akan memerintahkan **Terraform** untuk membuatnya secara otomatis lewat kode deklaratif!

---

## 2. Struktur Proyek Terraform Standar Industri

Di dunia kerja, kode Terraform biasanya dipecah menjadi 3 file agar rapi:

```
terraform/
├── main.tf        --> Berisi definisi resource yang ingin dibangun (Bucket GCS)
├── variables.tf   --> Berisi variabel (Project ID, Region, Nama Bucket) agar fleksibel
└── outputs.tf     --> Berisi data keluaran yang ingin ditampilkan (URL Bucket)
```

---

## 3. Langkah Praktik di Google Cloud Shell

Buka terminal **Google Cloud Shell** Anda dan ikuti langkah berikut:

### Langkah 1: Buat Folder Kerja & File Terraform
Jalankan blok perintah ini di Cloud Shell:

```bash
mkdir -p ~/tbs-terraform && cd ~/tbs-terraform

# 1. Buat file main.tf
cat << 'EOF' > main.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Membuat Google Cloud Storage Bucket untuk Backup Penjualan
resource "google_storage_bucket" "tbs_backup_bucket" {
  name          = "${var.project_id}-tbs-sales-backup"
  location      = "ASIA-SOUTHEAST2" # Region Jakarta
  storage_class = "STANDARD"
  force_destroy = true              # Memudahkan penghapusan saat eksperimen selesai

  uniform_bucket_level_access = true

  versioning {
    enabled = true                  # Riwayat versi backup aman
  }
}
EOF

# 2. Buat file variables.tf
cat << 'EOF' > variables.tf
variable "project_id" {
  description = "Project ID Google Cloud Anda"
  type        = string
  default     = "the-byway-487902-m9"
}

variable "region" {
  description = "Region default infrastruktur"
  type        = string
  default     = "asia-southeast2"
}
EOF

# 3. Buat file outputs.tf
cat << 'EOF' > outputs.tf
output "bucket_name" {
  description = "Nama Bucket yang berhasil dibuat"
  value       = google_storage_bucket.tbs_backup_bucket.name
}

output "bucket_url" {
  description = "URL akses Google Cloud Storage"
  value       = google_storage_bucket.tbs_backup_bucket.url
}
EOF
```

---

### Langkah 2: Inisialisasi Provider (`terraform init`)
Jalankan perintah ini untuk mengunduh modul resmi Google Cloud:

```bash
terraform init
```
*(Tunggu beberapa detik sampai muncul tulisan hijau: `Terraform has been successfully initialized!`)*

---

### Langkah 3: Simulasi Perubahan (`terraform plan`)
Jalankan perintah dry-run:

```bash
terraform plan
```
Perhatikan outputnya! Terraform akan menampilkan tanda plus hijau (**`+ create`**) dan merangkum di bagian bawah:
```
Plan: 1 to add, 0 to change, 0 to destroy.
```
Artinya: Terraform tahu bahwa ia akan menambahkan **1 resource baru** tanpa mengubah atau merusak resource yang sudah ada!

---

### Langkah 4: Eksekusi Pembangunan (*Apply*)
Jalankan eksekusi nyata:

```bash
terraform apply -auto-approve
```

Dalam waktu **3 sampai 5 detik**, bucket penyimpanan resmi TBS Food di Jakarta akan langsung tercipta di Google Cloud!

---

### Langkah 5: Pembuktian Siklus Hidup (*Destroy*)
Jika suatu hari Anda ingin menghapus seluruh resource yang dibuat oleh Terraform tanpa takut ada sisa biaya tersembunyi, Anda cukup mengetik:

```bash
terraform destroy -auto-approve
```
Semua yang dibuat di `main.tf` akan dihapus bersih seketika!

