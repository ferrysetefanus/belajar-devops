# Modul 2.5: Integrasi Database PostgreSQL di Compute Engine (e2-micro Always Free)

Dokumentasi ini adalah bagian lanjutan dari **Fase 2: Implementasi GCP Hemat Biaya & CI/CD Pipeline** pada [ROADMAP.md](../../ROADMAP.md).

---

## 1. Arsitektur Database 100% Gratis Selamanya di GCP

Google Cloud memiliki kebijakan **Always Free Tier**:
* 1 VM tipe **`e2-micro`** gratis setiap bulan.
* 30 GB Standard Persistent Disk gratis.
* Wajib dibuat di salah satu region US: `us-central1` (Iowa), `us-east1` (South Carolina), atau `us-west1` (Oregon).

Kita akan memanfaatkan VM gratis ini sebagai **Dedicated PostgreSQL Database Server** untuk menyimpan seluruh data penjualan TBS Food, lalu menghubungkannya ke Web Dashboard di Cloud Run.

```mermaid
flowchart LR
    User["Tim Kantor (Browser)"] -->|HTTPS| CR["Google Cloud Run (Jakarta)\n(tbs-sales-dashboard)"]
    CR -->|Koneksi Port 5432 (Internet/VPC)| VM["Compute Engine (us-central1)\n(tbs-db-vm - e2-micro)\nBiaya: Rp 0 Selamanya"]
    VM --> PG[("Container PostgreSQL\ntbs_sales_db")]
    PG --> Disk[("Volume 30GB Permanen")]
```

---

## 2. Langkah 1: Membuat VM `e2-micro` via Cloud Shell

Jalankan perintah ini di **Google Cloud Shell** untuk membuat server VM gratis:

```bash
gcloud compute instances create tbs-db-vm \
    --project=the-byway-487902-m9 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --image-family=debian-12 \
    --image-project=debian-cloud \
    --tags=postgres-server
```

---

## 3. Langkah 2: Buka Firewall Port 5432 untuk PostgreSQL

Secara default, Google memblokir semua port luar demi keamanan. Kita perlu membuka port 5432:

```bash
gcloud compute firewall-rules create allow-postgres \
    --project=the-byway-487902-m9 \
    --allow=tcp:5432 \
    --target-tags=postgres-server \
    --description="Izinkan akses port PostgreSQL"
```

---

## 4. Langkah 3: Masuk ke VM via SSH & Pasang Container PostgreSQL

Di Cloud Shell, ketik perintah ini untuk masuk ke dalam server VM baru Anda:

```bash
gcloud compute ssh tbs-db-vm --zone=us-central1-a
```
*(Jika pertama kali, tekan Enter untuk passphrase kosong).*

Setelah Anda berada di dalam terminal VM (`user@tbs-db-vm:~$`), jalankan instalasi Docker dan nyalakan PostgreSQL:

```bash
# 1. Update paket & install docker
sudo apt-get update && sudo apt-get install -y docker.io

# 2. Jalankan container PostgreSQL dengan data volume permanen
sudo docker run -d \
    --name postgres-tbs \
    --restart=always \
    -p 5432:5432 \
    -e POSTGRES_USER=tbs_admin \
    -e POSTGRES_PASSWORD=SecretPassword123 \
    -e POSTGRES_DB=tbs_sales_db \
    -v /var/lib/postgresql/data:/var/lib/postgresql/data \
    postgres:16-alpine

# 3. Verifikasi apakah container sudah hidup
sudo docker ps
```

Ketik `exit` untuk kembali ke terminal Google Cloud Shell biasa.

---

## 5. Langkah 4: Hubungkan Cloud Run Dashboard ke Database Ini

1. Catat **EXTERNAL_IP** dari VM `tbs-db-vm` Anda dengan mengetik:
   ```bash
   gcloud compute instances describe tbs-db-vm \
       --zone=us-central1-a \
       --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
   ```
2. Inject IP tersebut ke Cloud Run service Anda:
   ```bash
   DB_IP=$(gcloud compute instances describe tbs-db-vm --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

   gcloud run services update tbs-sales-dashboard \
       --region=asia-southeast2 \
       --update-env-vars DB_HOST=$DB_IP,DB_PORT=5432,DB_NAME=tbs_sales_db,DB_USER=tbs_admin,DB_PASSWORD=SecretPassword123
   ```

---

## 6. Verifikasi Akhir di Browser

Buka kembali URL Cloud Run Anda:  
👉 `https://tbs-sales-dashboard-908500337020.asia-southeast2.run.app`

Status pada respon JSON akan otomatis berubah menjadi:
```json
"database_connection": {
    "configured": true,
    "host": "34.xxx.xxx.xxx",
    "status": "CONNECTED_TO_DOCKER_NETWORK"
}
```
Database produksi 100% gratis Anda kini telah terintegrasi!
