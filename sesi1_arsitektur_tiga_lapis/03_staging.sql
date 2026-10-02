-- =====================================================================
-- SESI 1 · Langkah 3 — Menyalin kedua sumber ke STAGING, apa adanya
-- Aturan staging: SALIN, JANGAN PERBAIKI.
-- Jalankan:  mariadb -u root -p --local-infile=1 < 03_staging.sql
-- =====================================================================
USE staging_toko;

DROP TABLE IF EXISTS stg_penjualan_kasir;
DROP TABLE IF EXISTS stg_penjualan_barat;

-- ---------------------------------------------------------------------
-- Sumber 1: database kasir (Cabang Pusat & Timur)
-- Struktur sumber ternormalisasi, di staging kita ratakan jadi satu tabel.
-- ---------------------------------------------------------------------
CREATE TABLE stg_penjualan_kasir AS
SELECT n.id_nota,
       n.tanggal,
       c.nama_cabang,
       c.kota                AS kota_cabang,
       p.nama_produk,
       p.kategori,
       i.jumlah,
       p.harga               AS harga_satuan,
       n.id_pelanggan
FROM sumber_kasir.nota_item i
JOIN sumber_kasir.nota   n ON i.id_nota   = n.id_nota
JOIN sumber_kasir.produk p ON i.id_produk = p.id_produk
JOIN sumber_kasir.cabang c ON n.id_cabang = c.id_cabang;

-- ---------------------------------------------------------------------
-- Sumber 2: ekspor Excel Cabang Barat
-- SEMUA kolom bertipe teks: di staging kita belum tahu isinya bersih atau tidak.
-- ---------------------------------------------------------------------
CREATE TABLE stg_penjualan_barat (
  no_nota      VARCHAR(20),
  tanggal      VARCHAR(20),
  nama_produk  VARCHAR(60),
  jumlah       VARCHAR(10),
  harga_satuan VARCHAR(20),
  id_pelanggan VARCHAR(10)
);

-- PENTING: jalankan klien MySQL dari folder praktikum-dw (folder paling
-- luar), karena path di bawah ini dihitung dari tempat kamu berdiri,
-- bukan dari letak berkas SQL ini.
LOAD DATA LOCAL INFILE 'data/penjualan_barat.csv'
INTO TABLE stg_penjualan_barat
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT COUNT(*) AS baris_kasir FROM stg_penjualan_kasir;
SELECT COUNT(*) AS baris_barat FROM stg_penjualan_barat;
