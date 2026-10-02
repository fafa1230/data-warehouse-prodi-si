-- =====================================================================
-- SESI 2 · Langkah 2 — Membuat TABEL FAKTA
-- GRAIN: satu baris mewakili penjualan satu produk pada satu nota.
-- Materi: Minggu 4-5 (fakta, dimensi, grain, degenerate dimension)
-- Jalankan:  mariadb -u root -p < 02_fakta.sql
-- =====================================================================
USE dw_toko;

DROP TABLE IF EXISTS fact_penjualan;

CREATE TABLE fact_penjualan (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  -- kunci ke dimensi
  tanggal       DATE        NOT NULL,
  nama_produk   VARCHAR(50) NOT NULL,
  nama_cabang   VARCHAR(50) NOT NULL,
  id_pelanggan  INT         NOT NULL,
  -- degenerate dimension: nomor nota tidak punya tabel dimensi sendiri
  no_nota       VARCHAR(20) NOT NULL,
  -- ukuran (measure)
  jumlah        INT NOT NULL,   -- additive
  harga_satuan  INT NOT NULL,   -- NON-additive, jangan pernah di-SUM
  total         INT NOT NULL,   -- additive
  FOREIGN KEY (tanggal)      REFERENCES dim_tanggal(tanggal),
  FOREIGN KEY (nama_produk)  REFERENCES dim_produk(nama_produk),
  FOREIGN KEY (nama_cabang)  REFERENCES dim_cabang(nama_cabang),
  FOREIGN KEY (id_pelanggan) REFERENCES dim_pelanggan(id_pelanggan)
);

-- COALESCE(id_pelanggan, 0): transaksi tanpa identitas diarahkan ke
-- baris "Tanpa Pelanggan", bukan dibuang.
INSERT INTO fact_penjualan
  (tanggal, nama_produk, nama_cabang, id_pelanggan, no_nota,
   jumlah, harga_satuan, total)
SELECT tanggal, nama_produk, nama_cabang,
       COALESCE(id_pelanggan, 0),
       no_nota, jumlah, harga_satuan, total
FROM penjualan_bersih;

SELECT COUNT(*) AS baris_fakta, SUM(total) AS omzet FROM fact_penjualan;
