-- =====================================================================
-- SESI 1 · Langkah 1 — Membuat tiga lapis arsitektur
-- Materi: Minggu 3 (Arsitektur Data Warehouse)
-- Jalankan:  mariadb -u root -p < 01_buat_lapisan.sql
-- =====================================================================

DROP DATABASE IF EXISTS sumber_kasir;
DROP DATABASE IF EXISTS staging_toko;
DROP DATABASE IF EXISTS dw_toko;

CREATE DATABASE sumber_kasir;   -- Lapis 1: sistem sumber (aplikasi kasir)
CREATE DATABASE staging_toko;   -- Lapis 2: penampungan mentah
CREATE DATABASE dw_toko;        -- Lapis 3: data warehouse

-- Tabel di sistem sumber. Bentuknya ternormalisasi, khas aplikasi harian.
USE sumber_kasir;

CREATE TABLE cabang (
  id_cabang   INT PRIMARY KEY,
  nama_cabang VARCHAR(50) NOT NULL,
  kota        VARCHAR(50) NOT NULL
);

CREATE TABLE produk (
  id_produk   INT PRIMARY KEY,
  nama_produk VARCHAR(50) NOT NULL,
  kategori    VARCHAR(20) NOT NULL,
  harga       INT NOT NULL
);

CREATE TABLE pelanggan (
  id_pelanggan   INT PRIMARY KEY,
  nama_pelanggan VARCHAR(60) NOT NULL,
  kota           VARCHAR(50) NOT NULL,
  tanggal_daftar DATE NOT NULL
);

CREATE TABLE nota (
  id_nota      INT PRIMARY KEY,
  tanggal      DATE NOT NULL,
  id_cabang    INT NOT NULL,
  id_pelanggan INT NULL,
  FOREIGN KEY (id_cabang) REFERENCES cabang(id_cabang),
  FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan)
);

CREATE TABLE nota_item (
  id_item   INT AUTO_INCREMENT PRIMARY KEY,
  id_nota   INT NOT NULL,
  id_produk INT NOT NULL,
  jumlah    INT NOT NULL,
  FOREIGN KEY (id_nota) REFERENCES nota(id_nota),
  FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
);

INSERT INTO cabang VALUES
  (1, 'Cabang Pusat', 'Semarang'),
  (2, 'Cabang Timur', 'Semarang'),
  (3, 'Cabang Barat', 'Ungaran');

INSERT INTO produk VALUES
  (1, 'Roti Coklat',  'Roti',  8000),
  (2, 'Roti Keju',    'Roti',  9000),
  (3, 'Roti Sobek',   'Roti', 15000),
  (4, 'Donat Gula',   'Donat', 5000),
  (5, 'Donat Coklat', 'Donat', 6000),
  (6, 'Bolu Pandan',  'Kue',  22000),
  (7, 'Brownies',     'Kue',  25000),
  (8, 'Lapis Legit',  'Kue',  45000);

SELECT 'Tiga database dan tabel sumber berhasil dibuat.' AS status;
