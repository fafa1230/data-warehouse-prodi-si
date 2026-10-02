-- =====================================================================
-- SESI 2 · Langkah 1 — Membuat TABEL DIMENSI
-- Materi: Minggu 4-5 (dimensional modeling, star schema)
-- Jalankan:  mariadb -u root -p < 01_dimensi.sql
-- =====================================================================
USE dw_toko;

DROP TABLE IF EXISTS fact_penjualan;
DROP TABLE IF EXISTS dim_tanggal;
DROP TABLE IF EXISTS dim_produk;
DROP TABLE IF EXISTS dim_cabang;
DROP TABLE IF EXISTS dim_pelanggan;

-- ---------------------------------------------------------------------
-- DIMENSI TANGGAL
-- Dibuat sendiri untuk SATU TAHUN PENUH, bukan hanya tanggal yang ada
-- transaksinya. Tujuannya supaya laporan tetap bisa menampilkan hari
-- yang sama sekali tidak ada penjualan.
-- ---------------------------------------------------------------------
CREATE TABLE dim_tanggal (
  tanggal     DATE PRIMARY KEY,
  tahun       INT NOT NULL,
  bulan       INT NOT NULL,
  nama_bulan  VARCHAR(15) NOT NULL,
  hari        INT NOT NULL,
  nama_hari   VARCHAR(15) NOT NULL,
  minggu_ke   INT NOT NULL,
  kuartal     INT NOT NULL,
  akhir_pekan VARCHAR(5) NOT NULL
);

INSERT INTO dim_tanggal
WITH RECURSIVE deret AS (
  SELECT DATE('2026-01-01') AS tgl
  UNION ALL
  SELECT tgl + INTERVAL 1 DAY FROM deret WHERE tgl < '2026-12-31'
)
SELECT tgl,
       YEAR(tgl), MONTH(tgl), MONTHNAME(tgl),
       DAY(tgl),  DAYNAME(tgl), WEEK(tgl, 1), QUARTER(tgl),
       CASE WHEN DAYOFWEEK(tgl) IN (1, 7) THEN 'Ya' ELSE 'Tidak' END
FROM deret;

-- ---------------------------------------------------------------------
-- DIMENSI PRODUK
-- Kolom kategori diambil dari sistem sumber; kolom kelompok_harga
-- adalah atribut BARU yang tidak ada di sumber mana pun.
-- ---------------------------------------------------------------------
CREATE TABLE dim_produk (
  nama_produk    VARCHAR(50) PRIMARY KEY,
  kategori       VARCHAR(20) NOT NULL,
  harga_berlaku  INT NOT NULL,
  kelompok_harga VARCHAR(20) NOT NULL
);

INSERT INTO dim_produk
SELECT nama_produk, kategori, harga,
       CASE WHEN harga < 10000 THEN 'Murah'
            WHEN harga < 25000 THEN 'Sedang'
            ELSE 'Mahal' END
FROM sumber_kasir.produk;

-- ---------------------------------------------------------------------
-- DIMENSI CABANG
-- ---------------------------------------------------------------------
CREATE TABLE dim_cabang (
  nama_cabang VARCHAR(50) PRIMARY KEY,
  kota        VARCHAR(50) NOT NULL
);

INSERT INTO dim_cabang
SELECT nama_cabang, kota FROM sumber_kasir.cabang;

-- ---------------------------------------------------------------------
-- DIMENSI PELANGGAN
-- Baris id 0 dipakai untuk pembeli yang tidak menyebutkan identitas.
-- Tanpa baris ini, transaksi tunai akan hilang dari laporan.
-- ---------------------------------------------------------------------
CREATE TABLE dim_pelanggan (
  id_pelanggan   INT PRIMARY KEY,
  nama_pelanggan VARCHAR(60) NOT NULL,
  kota           VARCHAR(50) NOT NULL,
  tanggal_daftar DATE NULL
);

INSERT INTO dim_pelanggan VALUES (0, 'Tanpa Pelanggan', '-', NULL);

INSERT INTO dim_pelanggan
SELECT id_pelanggan, nama_pelanggan, kota, tanggal_daftar
FROM sumber_kasir.pelanggan;

SELECT (SELECT COUNT(*) FROM dim_tanggal)   AS dim_tanggal,
       (SELECT COUNT(*) FROM dim_produk)    AS dim_produk,
       (SELECT COUNT(*) FROM dim_cabang)    AS dim_cabang,
       (SELECT COUNT(*) FROM dim_pelanggan) AS dim_pelanggan;
