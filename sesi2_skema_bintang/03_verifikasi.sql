-- =====================================================================
-- SESI 2 · Langkah 3 — TITIK PERIKSA skema bintang
-- Jalankan:  mariadb -u root -p -t < 03_verifikasi.sql
-- =====================================================================
USE dw_toko;

SELECT '1. GRAIN: tidak boleh ada nota+produk yang kembar' AS pemeriksaan;
SELECT no_nota, nama_produk, COUNT(*) AS n
FROM fact_penjualan
GROUP BY no_nota, nama_produk
HAVING n > 1;

SELECT '2. Jumlah baris fakta dan omzet harus sama dengan Sesi 1' AS pemeriksaan;
SELECT COUNT(*) AS baris, SUM(total) AS omzet FROM fact_penjualan;

SELECT '3. Omzet per kategori (butuh join ke dim_produk)' AS pemeriksaan;
SELECT p.kategori, SUM(f.jumlah) AS potong, SUM(f.total) AS omzet
FROM fact_penjualan f
JOIN dim_produk p ON f.nama_produk = p.nama_produk
GROUP BY p.kategori
ORDER BY omzet DESC;

SELECT '4. Hari kerja vs akhir pekan (butuh join ke dim_tanggal)' AS pemeriksaan;
SELECT t.akhir_pekan,
       COUNT(DISTINCT t.tanggal) AS jumlah_hari,
       SUM(f.total)              AS omzet,
       ROUND(SUM(f.total) / COUNT(DISTINCT t.tanggal)) AS omzet_per_hari
FROM fact_penjualan f
JOIN dim_tanggal t ON f.tanggal = t.tanggal
GROUP BY t.akhir_pekan;

SELECT '5. Hari tanpa penjualan (LEFT JOIN dari dimensi ke fakta)' AS pemeriksaan;
SELECT COUNT(*) AS hari_tanpa_penjualan
FROM dim_tanggal t
LEFT JOIN fact_penjualan f ON t.tanggal = f.tanggal
WHERE f.id IS NULL;

SELECT '6. Jebakan ukuran NON-ADDITIVE' AS pemeriksaan;
SELECT SUM(harga_satuan)                AS jangan_pernah_di_sum,
       ROUND(AVG(harga_satuan))         AS rata_rata_tanpa_bobot,
       ROUND(SUM(total) / SUM(jumlah))  AS harga_rata_rata_benar
FROM fact_penjualan;

SELECT '7. Sepuluh pelanggan dengan belanja terbesar' AS pemeriksaan;
SELECT pl.nama_pelanggan, pl.kota,
       COUNT(DISTINCT f.no_nota) AS jumlah_nota,
       SUM(f.total)              AS total_belanja
FROM fact_penjualan f
JOIN dim_pelanggan pl ON f.id_pelanggan = pl.id_pelanggan
WHERE pl.id_pelanggan <> 0
GROUP BY pl.nama_pelanggan, pl.kota
ORDER BY total_belanja DESC
LIMIT 10;
