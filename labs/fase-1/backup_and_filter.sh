#!/usr/bin/env bash
# ==============================================================================
# Script Name : backup_and_filter.sh
# Purpose     : Otomasi backup log transaksi penjualan & filter baris error
# Author      : DevOps TBS Food Learner
# Usage       : ./backup_and_filter.sh <path_to_log_file>
# ==============================================================================

# Aktifkan mode proteksi standar produksi
set -euo pipefail

# 1. Validasi Argumen Input
if [ "$#" -lt 1 ]; then
    echo "=========================================================="
    echo "❌ PENGGUNAAN SALAH!"
    echo "Format  : $0 <path_file_log>"
    echo "Contoh  : $0 labs/fase-1/sales_transactions.log"
    echo "=========================================================="
    exit 1
fi

INPUT_LOG="$1"

# 2. Cek keberadaan file log
if [ ! -f "$INPUT_LOG" ]; then
    echo "❌ ERROR: File input '$INPUT_LOG' tidak ditemukan!" >&2
    exit 1
fi

# 3. Setup Direktori Output
BASE_DIR="$(dirname "$0")"
BACKUP_DIR="${BASE_DIR}/backups"
TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"

mkdir -p "$BACKUP_DIR"

REPORT_FILE="${BACKUP_DIR}/incident_report_${TIMESTAMP}.log"
ARCHIVE_FILE="${BACKUP_DIR}/sales_log_archive_${TIMESTAMP}.tar.gz"

echo "=========================================================="
echo "🚀 MEMULAI PROSES OTOMASI LOG & BACKUP PENJUALAN"
echo "Target File : $INPUT_LOG"
echo "Waktu       : $(date)"
echo "=========================================================="

# 4. Filter baris ERROR ke incident report
echo "🔍 [1/3] Memindai baris [ERROR]..."
grep -i "\[ERROR\]" "$INPUT_LOG" > "$REPORT_FILE" || true

# Hitung jumlah error yang ditemukan
ERROR_COUNT=$(wc -l < "$REPORT_FILE")

if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "⚠️  PERINGATAN: Ditemukan $ERROR_COUNT error pada log!"
    echo "    Laporan insiden disimpan ke: $REPORT_FILE"
else
    echo "✅ Tidak ada error ditemukan dalam log transaksi."
    rm -f "$REPORT_FILE"
fi

# 5. Kompresi log mentah ke arsip tar.gz
echo "📦 [2/3] Mengompresi log mentah ke format tar.gz..."
tar -czf "$ARCHIVE_FILE" -C "$(dirname "$INPUT_LOG")" "$(basename "$INPUT_LOG")"
echo "    Arsip berhasil dibuat: $ARCHIVE_FILE"

# 6. Ringkasan Ukuran & Status
echo "📊 [3/3] Ringkasan Penyimpanan:"
ls -lh "$ARCHIVE_FILE"

echo "=========================================================="
echo "🎉 PROSES SELESAI DENGAN SUKSES (Exit Code: 0)"
echo "=========================================================="
exit 0

