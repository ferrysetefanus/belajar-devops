# Modul 3.1: Konsep Infrastructure as Code (IaC) & Dasar Terraform

Dokumentasi ini adalah bagian awal dari **Fase 3: Infrastructure as Code (IaC) & Observability** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Dari "ClickOps" Menuju "Infrastructure as Code" (IaC)

Selama Fase 2, Anda membuat resource di Google Cloud dengan dua cara:
1. Mengetik perintah CLI `gcloud` di terminal Cloud Shell.
2. Mengklik menu di Google Cloud Console di browser (*sering dijuluki "ClickOps"*).

### Masalah Besar dengan "ClickOps" & Perintah Manual di Dunia Kerja:
* **Tidak Ada Rekam Jejak (*Audit Trail*):** Siapa yang mengubah ukuran RAM Cloud Run minggu lalu? Tidak ada yang tahu.
* **Sulit Direplikasi (*Cannot Reproduce*):** Jika besok manajemen TBS Food meminta Anda membuat lingkungan baru bernama `tbs-staging` untuk uji coba, Anda harus mengulang kembali mengetik puluhan perintah manual dari awal. Sangat rentan lupa salah satu parameter atau salah klik.
* **Risiko Resource Terlantar (*Cost Leak*):** Sangat sering seorang engineer membuat VM atau disk eksperimen, lalu lupa menghapusnya dan tagihan terus berjalan berbulan-bulan.

**Solusi:**  
**Infrastructure as Code (IaC)** adalah filosofi di mana **seluruh server, firewall, database, dan service cloud Anda ditulis dalam bentuk file teks (kode)** dan disimpan rapi di Git.

---

## 2. Mengapa Terraform Menjadi Standar Emas Industri?

**Terraform** (dibuat oleh HashiCorp) adalah tool IaC paling populer di dunia karena 3 keunggulan mutlak:

1. **Bersifat Deklaratif (Bukan Imperatif):**  
   * *Imperatif (Cara Lama):* Anda mendikte langkah-langkahnya: *"Buat VM, lalu tunggu 10 detik, lalu buka port 5432..."*
   * *Deklaratif (Terraform):* Anda cukup menyatakan hasil akhirnya: *"Saya ingin ada 1 VM e2-micro dengan tag postgres-server."* Terraform yang akan mencari tahu sendiri cara mewujudkannya secara efisien.
2. **Cloud-Agnostic (Bisa untuk Semua Cloud):**  
   Sintaks Terraform (disebut **HCL - HashiCorp Configuration Language**) sama persis baik saat Anda mengontrol **Google Cloud (GCP)**, **Amazon Web Services (AWS)**, maupun **Microsoft Azure**.
3. **Simulasi Sebelum Eksekusi (*Dry Run Plan*):**  
   Sebelum mengubah apa pun di cloud nyata, Terraform bisa memperlihatkan kalkulasi detail apa yang akan ditambah (`+`), diubah (`~`), atau dihapus (`-`).

---

## 3. Tritunggal Perintah Wajib Terraform

Hanya ada 4 perintah utama yang dipakai oleh DevOps Engineer setiap hari:

```
[1. terraform init]  --->  [2. terraform plan]  --->  [3. terraform apply]  --->  [4. terraform destroy]
 (Download Plugin)          (Simulasi Dry-Run)        (Eksekusi Nyata)             (Bersihkan Semua)
```

| Perintah | Fungsi | Analogi Arsitek Bangunan |
| :--- | :--- | :--- |
| `terraform init` | Mengunduh provider plugin (misal modul resmi Google Cloud). | Menyiapkan peralatan tukang & material. |
| `terraform plan` | Menampilkan simulasi perubahan tanpa menyentuh server nyata. | Membuat cetak biru (*blueprint*) dan mengecek ke klien. |
| `terraform apply`| Mengeksekusi pembuatan/perubahan server di Google Cloud. | Tukang mulai membangun gedung sesuai cetak biru. |
| `terraform destroy`| Menghapus seluruh server yang tercatat di kode tanpa sisa biaya. | Merobohkan bangunan dan membersihkan lahan. |

---

## 4. Konsep Kunci: "State File" (`terraform.tfstate`)

Bagaimana Terraform tahu bahwa VM `tbs-db-vm` sudah pernah dibuat kemarin dan tidak perlu dibuat ulang hari ini?

Jawabannya adalah **`terraform.tfstate`**:
* Sebuah file JSON yang menjadi "buku catatan rahasia" Terraform.
* File ini mencatat pemetaan antara **Kode yang Anda tulis** dengan **Resource fisik nyata di Google Cloud**.
* Setiap kali Anda menjalankan `terraform plan`, Terraform akan membandingkan:
  `Kode Anda` $\leftrightarrow$ `State File` $\leftrightarrow$ `Kondisi Nyata di GCP`.

---

## 5. Anatomi Kode Terraform Sederhana (`main.tf`)

Berikut contoh bagaimana 1 Virtual Machine didefinisikan dalam kode HCL:

```hcl
# 1. Tentukan Provider Cloud yang Digunakan
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "the-byway-487902-m9"
  region  = "asia-southeast2"
}

# 2. Definisikan VM Server Database (Sama persis seperti yang Anda buat manual!)
resource "google_compute_instance" "tbs_database" {
  name         = "tbs-db-vm"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 30
      type  = "pd-standard"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Memberikan IP Publik Eksternal
    }
  }

  tags = ["postgres-server"]
}
```

Perhatikan betapa indahnya kode di atas: **seluruh konfigurasi server fisik kini terbaca seperti dokumen tertulis yang bisa di-version control di Git!**

