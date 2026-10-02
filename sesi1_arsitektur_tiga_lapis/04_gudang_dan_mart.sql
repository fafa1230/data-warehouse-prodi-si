-- =====================================================================
-- SESI 1 · Langkah 4 — Membersihkan dan memuat ke DATA WAREHOUSE,
--                      lalu membuat DATA MART berupa view
-- Materi: Minggu 3 (staging -> gudang -> data mart)
-- Jalankan:  mariadb -u root -p < 04_gudang_dan_mart.sql
-- =====================================================================
USE dw_toko;

DROP VIEW  IF EXISTS mart_penjualan_cabang;
DROP VIEW  IF EXISTS mart_penjualan_produk;
DROP TABLE IF EXISTS penjualan_bersih;

-- GRAIN: satu baris = satu produk pada satu nota.
CREATE TABLE penjualan_bersih (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  no_nota       VARCHAR(20)  NOT NULL,
  tanggal       DATE         NOT NULL,
  nama_cabang   VARCHAR(50)  NOT NULL,
  kota_cabang   VARCHAR(50)  NOT NULL,
  nama_produk   VARCHAR(50)  NOT NULL,
  kategori      VARCHAR(20)  NOT NULL,
  jumlah        INT          NOT NULL,
  harga_satuan  INT          NOT NULL,
  total         INT          NOT NULL,
  id_pelanggan  INT          NULL,
  sumber        VARCHAR(10)  NOT NULL
);

-- ---------------------------------------------------------------------
-- Sumber 1 (kasir): sudah rapi, tinggal dihitung totalnya.
-- ---------------------------------------------------------------------
INSERT INTO penjualan_bersih
  (no_nota, tanggal, nama_cabang, kota_cabang, nama_produk,
   kategori, jumlah, harga_satuan, total, id_pelanggan, sumber)
SELECT CONCAT('NOTA-', id_nota),
       tanggal, nama_cabang, kota_cabang, nama_produk,
       kategori, jumlah, harga_satuan,
       jumlah * harga_satuan,
       id_pelanggan,
       'kasir'
FROM staging_toko.stg_penjualan_kasir;

-- ---------------------------------------------------------------------
-- Sumber 2 (Excel Cabang Barat): dibersihkan dulu.
--   1. tanggal dd/mm/yyyy  -> tipe DATE
--   2. nama produk dicocokkan ke tabel produk resmi (bukan sekadar diubah
--      huruf besar-kecilnya)
--   3. baris dengan jumlah kosong dibuang
--   4. baris duplikat dibuang dengan DISTINCT
-- ---------------------------------------------------------------------
INSERT INTO penjualan_bersih
  (no_nota, tanggal, nama_cabang, kota_cabang, nama_produk,
   kategori, jumlah, harga_satuan, total, id_pelanggan, sumber)
SELECT DISTINCT
       TRIM(s.no_nota),
       STR_TO_DATE(s.tanggal, '%d/%m/%Y'),
       'Cabang Barat',
       'Ungaran',
       p.nama_produk,
       p.kategori,
       CAST(s.jumlah AS UNSIGNED),
       CAST(s.harga_satuan AS UNSIGNED),
       CAST(s.jumlah AS UNSIGNED) * CAST(s.harga_satuan AS UNSIGNED),
       NULLIF(TRIM(s.id_pelanggan), ''),
       'excel'
FROM staging_toko.stg_penjualan_barat s
JOIN sumber_kasir.produk p
  ON UPPER(TRIM(s.nama_produk)) = UPPER(p.nama_produk)
WHERE TRIM(s.jumlah) <> '';

-- ---------------------------------------------------------------------
-- Lapisan penyajian: data mart berupa view di atas gudang.
-- ---------------------------------------------------------------------
CREATE VIEW mart_penjualan_produk AS
SELECT nama_produk,
       kategori,
       SUM(jumlah) AS total_terjual,
       SUM(total)  AS total_omzet
FROM penjualan_bersih
GROUP BY nama_produk, kategori;

CREATE VIEW mart_penjualan_cabang AS
SELECT nama_cabang,
       kota_cabang,
       COUNT(DISTINCT no_nota) AS jumlah_nota,
       SUM(total)              AS total_omzet
FROM penjualan_bersih
GROUP BY nama_cabang, kota_cabang;

SELECT 'Gudang data dan data mart selesai dibangun.' AS status;
