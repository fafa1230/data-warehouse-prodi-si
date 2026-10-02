#!/usr/bin/env bash
# =====================================================================
# jalankan_semua.sh — menjalankan keempat sesi inti berurutan dari nol.
#
# Sekali jalan, seluruh hasil praktikum terbentuk dari nol, jadi bisa
# dipakai sebagai pembanding hasil pekerjaanmu.
# Saat belajar, jalankan tiap langkah satu per satu, bukan lewat berkas ini.
#
# Pemakaian:
#   chmod +x jalankan_semua.sh
#   DW_USER=root DW_PASS=rahasia ./jalankan_semua.sh
# =====================================================================
set -e
cd "$(dirname "$0")"

DB_USER="${DW_USER:-root}"
DB_PASS="${DW_PASS:-}"
if [ -n "$DB_PASS" ]; then SANDI=(-p"$DB_PASS"); else SANDI=(); fi
MYSQL=(${DW_CLIENT:-mariadb} -u "$DB_USER" "${SANDI[@]}")

garis() { printf '\n========== %s ==========\n' "$1"; }

garis "PERSIAPAN · membuat data sumber"
python3 data/generate_data.py

garis "SESI 1 · Arsitektur Tiga Lapis dan Staging Area"
"${MYSQL[@]}" < sesi1_arsitektur_tiga_lapis/01_buat_lapisan.sql
"${MYSQL[@]}" sumber_kasir < data/seed_sumber.sql
"${MYSQL[@]}" --local-infile=1 < sesi1_arsitektur_tiga_lapis/03_staging.sql
"${MYSQL[@]}" < sesi1_arsitektur_tiga_lapis/04_gudang_dan_mart.sql
"${MYSQL[@]}" -t < sesi1_arsitektur_tiga_lapis/05_verifikasi.sql

garis "SESI 2 · Skema Bintang"
"${MYSQL[@]}" -t < sesi2_skema_bintang/01_dimensi.sql
"${MYSQL[@]}" -t < sesi2_skema_bintang/02_fakta.sql
"${MYSQL[@]}" -t < sesi2_skema_bintang/03_verifikasi.sql

garis "SESI 3 · ETL dengan Python"
python3 sesi3_etl_python/etl.py

garis "SESI 4 · Query OLAP dan Data Mart"
"${MYSQL[@]}" -t < sesi4_query_olap/olap.sql

garis "SELESAI"
echo "Keluaran CSV ada di folder keluaran/"
ls -1 keluaran/
