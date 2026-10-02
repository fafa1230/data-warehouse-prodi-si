-- =====================================================================
-- SESI 1 · Langkah 5 — TITIK PERIKSA
-- Cocokkan setiap angka dengan yang tertulis di modul.
-- Jalankan:  mariadb -u root -p -t < 05_verifikasi.sql
-- =====================================================================
USE dw_toko;

SELECT '1. Jumlah baris per lapisan' AS pemeriksaan;
SELECT (SELECT COUNT(*) FROM staging_toko.stg_penjualan_kasir) AS staging_kasir,
       (SELECT COUNT(*) FROM staging_toko.stg_penjualan_barat) AS staging_barat,
       (SELECT COUNT(*) FROM penjualan_bersih)                 AS gudang;

SELECT '2. Baris gudang per sumber' AS pemeriksaan;
SELECT sumber, COUNT(*) AS baris, SUM(total) AS omzet
FROM penjualan_bersih GROUP BY sumber;

SELECT '3. Tidak boleh ada tanggal atau produk yang gagal dibersihkan' AS pemeriksaan;
SELECT COUNT(*) AS baris_bermasalah
FROM penjualan_bersih
WHERE tanggal IS NULL OR nama_produk IS NULL OR jumlah <= 0;

SELECT '4. Nama produk harus tepat 8, bukan lebih' AS pemeriksaan;
SELECT COUNT(DISTINCT nama_produk) AS jumlah_produk FROM penjualan_bersih;

SELECT '5. Omzet seluruh toko' AS pemeriksaan;
SELECT COUNT(*) AS baris, COUNT(DISTINCT no_nota) AS nota, SUM(total) AS omzet
FROM penjualan_bersih;

SELECT '6. Isi data mart produk' AS pemeriksaan;
SELECT * FROM mart_penjualan_produk ORDER BY total_omzet DESC;

SELECT '7. Isi data mart cabang' AS pemeriksaan;
SELECT * FROM mart_penjualan_cabang ORDER BY total_omzet DESC;
