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

# Membuat Google Cloud Storage Bucket untuk Backup Penjualan TBS Food
resource "google_storage_bucket" "tbs_backup_bucket" {
  name          = "${var.project_id}-tbs-sales-backup"
  location      = "ASIA-SOUTHEAST2" # Region Jakarta
  storage_class = "STANDARD"
  force_destroy = true

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
