#!/usr/bin/env bash
import os
import sys
import time
import datetime

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "tbs_sales_db")
DB_USER = os.environ.get("DB_USER", "tbs_admin")

print("=" * 60, flush=True)
print("🚀 [ETL-WORKER] MEMULAI BATCH AGREGASI DATA PENJUALAN TBS FOOD", flush=True)
print(f"⏰ Waktu Eksekusi   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB", flush=True)
print(f"🔗 Target Database : {DB_HOST}:5432 (DB: {DB_NAME}, User: {DB_USER})", flush=True)
print("=" * 60, flush=True)

# 1. Ekstraksi (Extract)
print("📥 [1/3] Mengambil data transaksi mentah dari seluruh outlet...", flush=True)
time.sleep(2) # Simulasi query/proses penarikan data
dummy_records = [
    {"id": "TRX-001", "outlet": "Jakarta Barat", "total": 245000, "status": "SUCCESS"},
    {"id": "TRX-002", "outlet": "Bandung", "total": 580000, "status": "SUCCESS"},
    {"id": "TRX-003", "outlet": "Surabaya", "total": 120000, "status": "FAILED"},
    {"id": "TRX-004", "outlet": "Jakarta Selatan", "total": 310000, "status": "SUCCESS"},
    {"id": "TRX-005", "outlet": "Semarang", "total": 95000, "status": "SUCCESS"},
    {"id": "TRX-006", "outlet": "Tangerang", "total": 720000, "status": "SUCCESS"},
]
print(f"   -> Berhasil mengekstrak {len(dummy_records)} baris transaksi.", flush=True)

# 2. Transformasi (Transform)
print("🔄 [2/3] Mengagregasi total omset & validasi data...", flush=True)
time.sleep(2)
successful_trx = [r for r in dummy_records if r["status"] == "SUCCESS"]
total_omset = sum(r["total"] for r in successful_trx)
outlets_count = len(set(r["outlet"] for r in dummy_records))

print(f"   -> Total Transaksi Sukses : {len(successful_trx)} transaksi", flush=True)
print(f"   -> Total Revenue Hari Ini : Rp {total_omset:,.0f}".replace(",", "."), flush=True)
print(f"   -> Total Outlet Aktif     : {outlets_count} outlet", flush=True)

# 3. Pemuatan (Load)
print(f"💾 [3/3] Memperbarui tabel agregasi di Database {DB_HOST}...", flush=True)
time.sleep(1)
print("   -> Sinkronisasi data ke PostgreSQL selesai tanpa konflik.", flush=True)

print("=" * 60, flush=True)
print("🎉 [ETL-WORKER] BATCH SELESAI DENGAN SUKSES! (Status: EXIT 0)", flush=True)
print("=" * 60, flush=True)
sys.exit(0)
