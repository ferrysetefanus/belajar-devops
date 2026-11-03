output "bucket_name" {
  description = "Nama Bucket yang berhasil dibuat"
  value       = google_storage_bucket.tbs_backup_bucket.name
}

output "bucket_url" {
  description = "URL akses Google Cloud Storage"
  value       = google_storage_bucket.tbs_backup_bucket.url
}
