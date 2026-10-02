-- =====================================================================
-- SESI 4 · Query OLAP dan Data Mart
-- Materi: Minggu 13 (roll-up, drill-down, slice, dice, pivot)
-- Berjalan di atas tabel hasil Sesi 3 (berakhiran _py).
--
-- Jalankan dari folder praktikum-dw-inti:
--   mysql -u root -p -t < sesi4_query_olap/olap.sql
-- =====================================================================
USE dw_toko;

-- ---------------------------------------------------------------------
-- 0. View gabungan. Query berikutnya jadi pendek karena join panjangnya
--    sudah selesai di sini. Inilah bentuk paling sederhana data mart.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW v_penjualan AS
SELECT t.tanggal, t.tahun, t.bulan, t.nama_bulan, t.kuartal,
       t.nama_hari, t.akhir_pekan,
       p.nama_produk, p.kategori,
       c.nama_cabang, c.kota_cabang,
       pl.nama_pelanggan, pl.kota AS kota_pelanggan,
       f.no_nota, f.jumlah, f.harga_satuan, f.total
FROM fact_penjualan_py f
JOIN dim_tanggal_py   t  ON f.tanggal_key   = t.tanggal_key
JOIN dim_produk_py    p  ON f.produk_key    = p.produk_key
JOIN dim_cabang_py    c  ON f.cabang_key    = c.cabang_key
JOIN dim_pelanggan_py pl ON f.pelanggan_key = pl.pelanggan_key;

SELECT '=== 1. ROLL-UP: dari harian naik ke bulanan ===' AS operasi;

SELECT bulan, nama_bulan,
       COUNT(DISTINCT tanggal) AS jumlah_hari,
       COUNT(DISTINCT no_nota) AS jumlah_nota,
       SUM(jumlah)             AS potong,
       SUM(total)              AS omzet
FROM v_penjualan
GROUP BY bulan, nama_bulan
ORDER BY bulan;

SELECT '--- naik satu tingkat lagi: per kuartal ---' AS operasi;
SELECT kuartal, SUM(total) AS omzet FROM v_penjualan GROUP BY kuartal;

SELECT '=== 2. DRILL-DOWN: dari kategori turun ke produk ===' AS operasi;

SELECT kategori, SUM(total) AS omzet
FROM v_penjualan GROUP BY kategori ORDER BY omzet DESC;

SELECT '--- turun ke produk, khusus kategori Kue ---' AS operasi;
SELECT kategori, nama_produk, SUM(jumlah) AS potong, SUM(total) AS omzet
FROM v_penjualan
WHERE kategori = 'Kue'
GROUP BY kategori, nama_produk
ORDER BY omzet DESC;

SELECT '=== 3. SLICE: memotong SATU dimensi (bulan Februari saja) ===' AS operasi;

SELECT nama_cabang, COUNT(DISTINCT no_nota) AS nota, SUM(total) AS omzet
FROM v_penjualan
WHERE bulan = 2
GROUP BY nama_cabang
ORDER BY omzet DESC;

SELECT '=== 4. DICE: memotong BEBERAPA dimensi sekaligus ===' AS operasi;
SELECT '    (kategori Kue + Cabang Pusat + akhir pekan)' AS keterangan;

SELECT nama_produk, SUM(jumlah) AS potong, SUM(total) AS omzet
FROM v_penjualan
WHERE kategori = 'Kue'
  AND nama_cabang = 'Cabang Pusat'
  AND akhir_pekan = 'Ya'
GROUP BY nama_produk
ORDER BY omzet DESC;

SELECT '=== 5. PIVOT: memutar bulan dari baris menjadi kolom ===' AS operasi;

SELECT nama_cabang,
       SUM(CASE WHEN bulan = 1 THEN total ELSE 0 END) AS januari,
       SUM(CASE WHEN bulan = 2 THEN total ELSE 0 END) AS februari,
       SUM(CASE WHEN bulan = 3 THEN total ELSE 0 END) AS maret,
       SUM(total) AS kuartal_1
FROM v_penjualan
GROUP BY nama_cabang
ORDER BY kuartal_1 DESC;

SELECT '=== 6. SUBTOTAL OTOMATIS dengan WITH ROLLUP ===' AS operasi;
SELECT '    (baris SEMUA adalah subtotal dan total keseluruhan)' AS keterangan;

SELECT COALESCE(nama_cabang, 'SEMUA CABANG') AS cabang,
       COALESCE(kategori, 'semua kategori')  AS kategori,
       SUM(total) AS omzet
FROM v_penjualan
GROUP BY nama_cabang, kategori WITH ROLLUP;

SELECT '=== 7. FUNGSI WINDOW: peringkat dan total berjalan ===' AS operasi;
SELECT '    (dua produk terlaris di SETIAP cabang)' AS keterangan;

-- MySQL tidak punya QUALIFY, jadi hasil RANK dibungkus subquery dulu
-- baru disaring di WHERE.
SELECT nama_cabang, peringkat, nama_produk, omzet
FROM (
  SELECT nama_cabang, nama_produk, omzet,
         RANK() OVER (PARTITION BY nama_cabang ORDER BY omzet DESC) AS peringkat
  FROM (
    SELECT nama_cabang, nama_produk, SUM(total) AS omzet
    FROM v_penjualan
    GROUP BY nama_cabang, nama_produk
  ) x
) y
WHERE peringkat <= 2
ORDER BY nama_cabang, peringkat;

SELECT '--- omzet berjalan dari bulan ke bulan ---' AS operasi;

SELECT bulan, nama_bulan, omzet,
       SUM(omzet) OVER (ORDER BY bulan) AS omzet_berjalan
FROM (
  SELECT bulan, nama_bulan, SUM(total) AS omzet
  FROM v_penjualan GROUP BY bulan, nama_bulan
) z
ORDER BY bulan;

-- ---------------------------------------------------------------------
-- 8. DATA MART: menyimpan hasil yang sering dipakai sebagai view
--    supaya pengguna bisnis tidak perlu menulis query panjang.
-- ---------------------------------------------------------------------
SELECT '=== 8. Membuat data mart untuk pengguna bisnis ===' AS operasi;

CREATE OR REPLACE VIEW mart_bulanan AS
SELECT bulan, nama_bulan, nama_cabang, kategori,
       COUNT(DISTINCT no_nota) AS jumlah_nota,
       SUM(jumlah)             AS potong,
       SUM(total)              AS omzet
FROM v_penjualan
GROUP BY bulan, nama_bulan, nama_cabang, kategori;

SELECT * FROM mart_bulanan
WHERE nama_cabang = 'Cabang Pusat'
ORDER BY bulan, omzet DESC;
