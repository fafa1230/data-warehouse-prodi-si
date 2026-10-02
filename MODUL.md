# Modul Praktikum Data Warehouse — Paket Inti 4 Sesi

Program Studi Sistem Informasi · Mata Kuliah Data Warehouse (3 SKS)

Versi ringkas dari modul delapan sesi, disusun untuk waktu praktikum yang terbatas dan laptop berspesifikasi minimal. Empat sesi, satu studi kasus, data ratusan baris. Seluruh kode sudah diuji jalan dari nol sampai selesai.

## Apa Isi Paket Inti

Paket inti memadatkan delapan sesi praktikum menjadi empat, dan memperkecil datanya dari ribuan baris menjadi 560. Rantai gudang data tetap utuh dari nota kasir sampai laporan OLAP; yang dilepas adalah topik lanjutan yang bisa dibahas di kuliah tanpa praktikum.

![Alur empat sesi praktikum: Sesi 1 dan Sesi 3 menempuh dua jalan ke angka yang sama](modul-gambar/alur-4-sesi.png)

Perhatikan garis berwarna di sebelah kanan. Sesi 1 mengerjakan integrasi dengan SQL, Sesi 3 mengerjakan ulang pekerjaan yang sama dengan Python — dan keduanya harus berhenti di 560 baris dengan omzet 20.784.000. Kesamaan itu bukan kebetulan yang menyenangkan, tapi satu-satunya bukti bahwa aturan pembersihan ditegakkan konsisten di kedua jalur. Inilah inti pedagogis seluruh paket.

### Skala yang diperkecil, dan alasannya

|  | Paket 8 sesi | Paket inti |
| --- | --- | --- |
| Jumlah sesi | 8 | 4 |
| Periode data | Januari–Juli 2026 | Januari–Maret 2026 |
| Baris di gudang | 4.467 | 560 |
| Jenis produk | 10 | 8 |
| Pelanggan | 120 | 40 |
| Pustaka Python | 6 (termasuk scikit-learn, mlxtend) | 3 |
| Ukuran seluruh paket | puluhan MB sesudah terisi | di bawah 10 MB |

Tiga keputusan di tabel itu saling menopang. Memotong periode jadi satu kuartal membuat jumlah baris turun ke ratusan, sehingga setiap query selesai dalam hitungan detik di laptop lama. Membuang sesi visualisasi dan data mining menghapus kebutuhan matplotlib, scikit-learn dan mlxtend — tiga pustaka yang paling sering gagal dipasang di laptop berspesifikasi minimal. Dan mengulang seluruh praktikum dari nol kini cuma butuh dua menit, yang berarti kesalahan tidak lagi mahal.

Yang tidak dikurangi: kerumitan datanya. Ekspor Excel Cabang Barat tetap berantakan — tanggal berformat `dd/mm/yyyy`, nama produk dengan huruf besar-kecil yang tidak konsisten, 12 baris duplikat, 5 baris tanpa jumlah. Data yang lebih sedikit bukan berarti data yang lebih bersih, karena justru pembersihan itulah pelajarannya.

## Persiapan

Tiga perangkat saja, dan hanya satu di antaranya yang butuh unduhan besar.

| Perangkat | Keterangan | Dipakai di |
| --- | --- | --- |
| MySQL 8 atau MariaDB 10.4+ | tempat gudang data berdiri | Sesi 1, 2, 4 |
| Klien SQL | perintah `mysql`/`mariadb`; Workbench atau DBeaver kalau RAM lega | Sesi 1, 2, 4 |
| Python 3.9+ | hanya untuk satu skrip | Sesi 3 |

### Spesifikasi minimum laptop

| Komponen | Minimum | Nyaman |
| --- | --- | --- |
| RAM | 4 GB | 8 GB |
| Ruang disk kosong | 2 GB | 5 GB |
| Prosesor | dua inti | apa pun yang lebih baru |
| Sistem operasi | Windows 10, macOS 11, atau Linux — semuanya 64-bit | — |

Praktikumnya sendiri sangat ringan. Seluruh langkah SQL — membangun tiga lapis, memuat staging, menyusun skema bintang, sampai delapan query OLAP di Sesi 4 — masing-masing selesai di bawah 0,2 detik. Skrip ETL Sesi 3 yang paling berat, dan itu pun 1 sampai 3 detik dengan memori puncak 98 MB. Ketiga database di disk cuma 2 MB. Di laptop yang jauh lebih lambat, angka-angka ini tinggal dikalikan tiga sampai lima — tetap hitungan detik.

Yang memakan sumber daya justru perkakas di sekelilingnya: MariaDB yang sedang berjalan memakai sekitar 110 MB memori, ketiga pustaka Python menempati sekitar 140 MB di disk, sedangkan MySQL Workbench atau DBeaver bisa menghabiskan 300–500 MB memori sendirian.

### Kalau RAM laptopmu 4 GB

Tiga penyesuaian ini membuat praktikum tetap lancar:

1. Jalankan semua berkas SQL lewat perintah `mysql`, bukan lewat Workbench atau DBeaver. Seluruh perintah di modul ini memang sudah ditulis dalam bentuk itu, jadi tidak ada yang hilang.
2. Pasang MariaDB saja, bukan XAMPP. XAMPP ikut membawa Apache dan PHP yang sama sekali tidak dipakai di mata kuliah ini.
3. Tutup browser dan aplikasi lain selama praktikum berjalan.

Kalau RAM-mu di bawah 4 GB, atau laptopmu sudah sering berhenti merespons, pakai komputer laboratorium atau jalankan praktikum ini lewat GitHub Codespaces — di sana MariaDB dan Python berjalan di server, dan laptopmu cukup menjalankan browser.

Bagian pemasangan paling berat bukan menjalankannya, melainkan mengunduh dan memasang MariaDB serta Python. Di laptop berhard disk, langkah itu bisa belasan menit. Sesudah terpasang, praktikumnya tetap cepat.

Pustaka Python-nya tinggal tiga, dan ketiganya ringan:

```
pandas>=2.0
SQLAlchemy>=2.0
PyMySQL>=1.1
```

```bash
pip install -r requirements.txt
```

Paket 8 sesi menuntut matplotlib, scikit-learn dan mlxtend — ketiganya besar dan lambat dipasang di laptop lama. Paket inti tidak memakainya sama sekali, jadi pemasangan selesai dalam satu menit di koneksi biasa.

### Satu berkas yang perlu diubah

Buka `konfigurasi.py`, isi nama pengguna dan sandi MySQL-mu:

```python
DB_USER = os.environ.get("DW_USER", "root")
DB_PASS = os.environ.get("DW_PASS", "")
DB_HOST = os.environ.get("DW_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DW_PORT", 3306))
```

Seluruh skrip membaca dari berkas ini, jadi sandi hanya ditulis satu kali. Kalau tidak ingin mengubah berkas, titipkan lewat variabel lingkungan: `export DW_PASS=sandimu`.

### Periksa kesiapan sebelum mulai

```bash
python cek_pemasangan.py
```

Skrip ini memeriksa lima hal dan menyebutkan persis apa yang kurang beserta cara memperbaikinya: RAM dan sisa disk, versi Python, ketiga pustaka, kedua berkas data, dan koneksi ke MySQL. Jalankan ini lebih dulu di pertemuan pertama — satu menit di awal menghemat setengah jam menebak-nebak di tengah praktikum.

### Satu aturan yang sering dilupakan

Semua perintah dijalankan **dari folder `praktikum-dw-inti`**, bukan dari dalam folder sesi. Beberapa berkas menunjuk ke `data/penjualan_barat.csv` dengan jalur relatif, jadi posisi folder kerja menentukan berhasil atau tidaknya.

## Sesi 1 — Arsitektur Tiga Lapis dan Staging Area

Satu sesi ini membangun ketiga lapis sekaligus, jadi arsitektur Minggu 3 berdiri sebagai tiga database yang bisa kamu buka, bukan sebagai gambar di slide.

| Lapis | Database | Isinya |
| --- | --- | --- |
| Sumber | `sumber_kasir` | tabel ternormalisasi: cabang, produk, pelanggan, nota, nota\_item |
| Staging | `staging_toko` | salinan mentah kedua sumber, apa adanya |
| Gudang + mart | `dw_toko` | tabel `penjualan_bersih` + dua view data mart |

### Langkah 1 — tiga database berdiri

```sql
CREATE DATABASE sumber_kasir;   -- Lapis 1: sistem sumber (aplikasi kasir)
CREATE DATABASE staging_toko;   -- Lapis 2: penampungan mentah
CREATE DATABASE dw_toko;        -- Lapis 3: data warehouse
```

Tiga perintah ini saja sudah jadi bahan diskusi: mengapa gudang harus terpisah dari sumber? Jawabannya terasa sendiri di langkah 4, ketika query pembersihan berjalan berat dan kasir tetap tidak terganggu.

### Langkah 2 — dua sumber dengan dua bentuk berbeda

Cabang Pusat dan Timur masuk lewat database kasir yang rapi. Cabang Barat mengirim ekspor Excel yang sengaja dibuat berantakan: tanggal `30/01/2026`, nama produk kadang `ROTI KEJU`, kadang `roti keju`, kadang `  Roti Keju `, ditambah 12 baris duplikat dan 5 baris tanpa jumlah.

Inilah inti pelajaran integrasi: gudang data hampir selalu menerima lebih dari satu bentuk sumber.

### Langkah 3 — staging: salin, jangan perbaiki

```sql
CREATE TABLE stg_penjualan_barat (
  no_nota      VARCHAR(20),
  tanggal      VARCHAR(20),
  nama_produk  VARCHAR(60),
  jumlah       VARCHAR(10),
  harga_satuan VARCHAR(20),
  id_pelanggan VARCHAR(10)
);

LOAD DATA LOCAL INFILE 'data/penjualan_barat.csv'
INTO TABLE stg_penjualan_barat
FIELDS TERMINATED BY ',' ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

Semua kolom bertipe `VARCHAR`, termasuk `jumlah` dan `tanggal`. Ini bukan kemalasan, ini aturan staging: di lapis ini kita belum tahu isinya bersih atau tidak, jadi jangan sampai satu baris rusak menolak seluruh muatan. Tipe data yang benar ditegakkan nanti, di lapis gudang.

### Langkah 4 — pembersihan yang menegakkan empat aturan

```sql
INSERT INTO penjualan_bersih (...)
SELECT DISTINCT
       TRIM(s.no_nota),
       STR_TO_DATE(s.tanggal, '%d/%m/%Y'),
       'Cabang Barat', 'Ungaran',
       p.nama_produk,          -- nama resmi, dari tabel produk
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
```

Empat aturan sekaligus: `STR_TO_DATE` mengubah `dd/mm/yyyy` jadi tipe `DATE`, `DISTINCT` membuang 12 duplikat, `WHERE TRIM(s.jumlah) <> ''` membuang 5 baris tanpa jumlah, dan `JOIN` ke tabel `produk` menyeragamkan nama.

Aturan keempat itu yang paling sering salah dikerjakan. Cara naif adalah `INITCAP` atau judul-kasus manual, yang menghasilkan `Roti coklat` — beda satu huruf dari `Roti Coklat`, dan satu produk berubah jadi dua baris di laporan. Mencocokkan ke tabel resmi menutup celah itu untuk selamanya: nama yang dipakai di gudang **selalu** nama milik tabel `produk`, bukan nama yang diketik kasir.

Kolom `sumber` bernilai `kasir` atau `excel`. Kolom sekecil itu menyelamatkan banyak waktu ketika angka tidak cocok nanti — langsung kelihatan sumber mana yang bermasalah.

### Langkah 5 — titik periksa

| Pemeriksaan | Nilai benar |
| --- | --- |
| `stg_penjualan_kasir` | 389 |
| `stg_penjualan_barat` | 188 |
| `penjualan_bersih` | 560 |
| dari kasir / dari Excel | 389 / 171 |
| Baris bermasalah (tanggal NULL, jumlah ≤ 0) | 0 |
| Nama produk berbeda | 8 |
| Jumlah nota | 310 |
| Omzet satu kuartal | 20.784.000 |

Perhatikan jalur 188 → 171: lima baris hilang karena jumlahnya kosong, dua belas karena duplikat. Hitung sendiri 188 − 5 − 12 = 171 sebelum menjalankan query. Kalau hasilnya 188, `DISTINCT` lupa ditulis. Kalau 183, filter jumlah kosong jalan tapi duplikat belum dibuang.

Angka 8 di baris "nama produk berbeda" adalah titik periksa paling tajam di seluruh sesi. Kalau muncul 9, 10 atau lebih, berarti pencocokan nama gagal dan ada produk yang terpecah.

## Sesi 2 — Skema Bintang

Sesi ini mengubah satu tabel lebar `penjualan_bersih` menjadi satu tabel fakta dengan empat dimensi di sekelilingnya — bentuk bintang yang jadi bahasa bersama semua pembuat gudang data.

### Grain ditetapkan lebih dulu, sebelum satu kolom pun ditulis

> Satu baris di `fact_penjualan` mewakili **penjualan satu produk pada satu nota**.

Satu kalimat itu menentukan segalanya: ukuran mana yang boleh dijumlahkan, dimensi mana yang perlu ada, dan query mana yang mustahil dijawab. Nota berisi tiga produk menghasilkan tiga baris. Biasakan menulis kalimat grain di komentar paling atas berkas SQL-mu, sebelum `CREATE TABLE`.

### Dimensi tanggal dibuat sendiri, satu tahun penuh

```sql
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
```

Hasilnya 365 baris, padahal transaksi hanya ada di 90 hari. Itu disengaja. Dimensi tanggal dibuat untuk seluruh kalender, bukan hanya untuk hari yang ada penjualannya — karena pertanyaan "hari apa saja toko tidak menjual apa pun?" baru bisa dijawab kalau hari-hari kosong itu punya baris di dimensi.

Pemeriksaan nomor 5 di sesi ini membuktikannya: `LEFT JOIN` dari `dim_tanggal` ke fakta menemukan **275 hari tanpa penjualan**. Tanpa dimensi tanggal yang lengkap, angka itu tidak mungkin keluar dari query apa pun.

Dimensi produk juga menambah kolom yang tidak ada di sumber mana pun:

```sql
CASE WHEN harga < 10000 THEN 'Murah'
     WHEN harga < 25000 THEN 'Sedang'
     ELSE 'Mahal' END
```

Ini contoh paling kecil dari gagasan besar: dimensi bukan salinan tabel sumber, dimensi adalah tempat menaruh cara bisnis memandang sesuatu.

### Dua rancangan yang menyelamatkan laporan

```sql
-- Baris id 0 untuk pembeli yang tidak menyebutkan identitas
INSERT INTO dim_pelanggan VALUES (0, 'Tanpa Pelanggan', '-', NULL);
```

```sql
SELECT tanggal, nama_produk, nama_cabang,
       COALESCE(id_pelanggan, 0),   -- bukan dibuang, diarahkan
       no_nota, jumlah, harga_satuan, total
FROM penjualan_bersih;
```

Ada 167 baris transaksi tanpa identitas pembeli. Kalau `NULL` dibiarkan, `INNER JOIN` ke dimensi pelanggan akan menghapus 167 baris itu dan omzet laporan langsung meleset. Baris "Tanpa Pelanggan" membuat semua transaksi tetap ikut terhitung sambil tetap bisa dipisahkan.

Kolom `no_nota` tidak punya tabel dimensi sendiri — ia duduk di tabel fakta sebagai **degenerate dimension**. Tidak ada atribut lain yang bisa digantung padanya, jadi membuat `dim_nota` hanya akan jadi tabel satu kolom yang tidak berguna.

### Titik periksa

| Pemeriksaan | Nilai benar |
| --- | --- |
| `dim_tanggal` / `dim_produk` / `dim_cabang` / `dim_pelanggan` | 365 / 8 / 3 / 41 |
| `fact_penjualan` | 560 baris, omzet 20.784.000 |
| Nota + produk kembar | 0 baris |
| Omzet per kategori (Kue / Roti / Donat) | 13.801.000 / 5.166.000 / 1.817.000 |
| Omzet per hari: akhir pekan vs hari kerja | 301.808 vs 202.141 |
| Hari tanpa penjualan | 275 |

Dimensi pelanggan berisi 41 baris, bukan 40: empat puluh pelanggan ditambah satu baris "Tanpa Pelanggan". Periksa angka ini sebelum lanjut ke tabel fakta.

Angka omzet 20.784.000 harus **sama persis** dengan hasil Sesi 1. Memindahkan data ke skema bintang tidak boleh menambah atau mengurangi satu rupiah pun.

### Jebakan ukuran non-additive

```sql
SELECT SUM(harga_satuan)                AS jangan_pernah_di_sum,
       ROUND(AVG(harga_satuan))         AS rata_rata_tanpa_bobot,
       ROUND(SUM(total) / SUM(jumlah))  AS harga_rata_rata_benar
FROM fact_penjualan;
```

| Cara menghitung | Hasil | Benar? |
| --- | --- | --- |
| `SUM(harga_satuan)` | 8.870.000 | tidak bermakna apa pun |
| `AVG(harga_satuan)` | 15.839 | salah, tiap baris dihitung sama bobotnya |
| `SUM(total) / SUM(jumlah)` | 16.225 | benar |

Tiga angka dari satu tabel yang sama, dan hanya satu yang boleh masuk laporan. `jumlah` dan `total` bersifat additive — boleh dijumlahkan ke arah dimensi mana pun. `harga_satuan` tidak: menjumlahkan harga satuan tidak menghasilkan apa-apa, dan merata-ratakannya tanpa bobot memberi harga roti murah yang terjual banyak pengaruh yang sama dengan lapis legit yang terjual sedikit.

Selisih 15.839 melawan 16.225 memang kecil. Justru itu yang berbahaya: angka salah yang kelihatan masuk akal lolos dari pemeriksaan jauh lebih sering daripada angka salah yang jelas ngawur.

## Sesi 3 — ETL dengan Python

Sesi ini mengerjakan ulang pekerjaan Sesi 1, kali ini dengan Python. Satu berkas, `sesi3_etl_python/etl.py`, dengan tiga bagian yang diberi garis pemisah mencolok di dalam kode:

```python
#  BAGIAN 1  EXTRACT    tarik apa adanya dari MySQL dan dari CSV
#  BAGIAN 2  TRANSFORM  bersihkan, seragamkan, catat yang dibuang
#  BAGIAN 3  LOAD       muat dimensi dulu, baru fakta, terakhir indeks
```

Di paket 8 sesi ini terpecah jadi dua sesi dan tiga berkas. Di paket inti ketiganya dalam satu berkas yang dijalankan sekali — satu perintah, satu laporan, selesai dalam hitungan detik.

```bash
python sesi3_etl_python/etl.py
```

### Extract hanya menarik, tidak membersihkan

```python
def extract_barat() -> pd.DataFrame:
    # dtype=str itu disengaja, sikapnya sama dengan kolom VARCHAR di
    # staging Sesi 1: jangan memaksakan tipe data sebelum tahu isinya bersih.
    return pd.read_csv(cfg.DATA / "penjualan_barat.csv", dtype=str)
```

`dtype=str` adalah titik temu dengan Sesi 1. Di SQL kita memakai kolom `VARCHAR` untuk semuanya; di pandas kita memakai `dtype=str`. Prinsipnya identik, cuma alatnya berbeda. Alasan nyatanya: satu baris dengan jumlah kosong akan menggagalkan seluruh pembacaan kalau pandas dipaksa menebak tipe angka.

Alasan kedua yang lebih penting di dunia kerja: makin cepat extract selesai, makin singkat sistem kasir terganggu. Pembersihan bisa dikerjakan belakangan, di mesin kita sendiri.

### Transform mencatat setiap baris yang dibuang

```python
catatan = []          # log: (langkah, masuk, dibuang, keluar)

def lapor(langkah, masuk, keluar):
    catatan.append((langkah, masuk, masuk - keluar, keluar))
```

Fungsi tiga baris ini adalah bagian paling berharga di seluruh sesi. Keluarannya:

```
Langkah                                  masuk  dibuang  keluar
---------------------------------------------------------------
Kasir: menyamakan bentuk kolom             389        0     389
Excel: membuang baris tanpa jumlah         188        5     183
Excel: membuang baris duplikat             183       12     171
Excel: mencocokkan nama produk             171        0     171
---------------------------------------------------------------
HASIL AKHIR                                                 560
```

ETL yang hanya mencetak "selesai" tidak bisa dipercaya. Yang bisa dipercaya adalah ETL yang bisa ditanya: dari 188 baris, ke mana perginya 17? Tabel di atas menjawabnya baris per baris. Kalau kamu memakai ETL di skripsi, pertanyaan ini hampir pasti muncul di sidang, jadi siapkan lognya sejak awal.

Penyeragaman nama produk memakai cara yang sama dengan Sesi 1, bukan `.str.title()`:

```python
df["kunci"] = df["nama_produk"].str.strip().str.upper()
produk["kunci"] = produk["nama_produk"].str.upper()
df = df.merge(produk[["kunci", "nama_produk", "kategori"]],
              on="kunci", how="left", suffixes=("_asli", ""))
tidak_cocok = int(df["nama_produk"].isna().sum())
if tidak_cocok:
    print(f"PERINGATAN: {tidak_cocok} baris tidak cocok ke tabel produk.")
```

Perhatikan `how="left"` lalu hitung yang `NaN`. Kalau memakai `how="inner"`, baris yang gagal dicocokkan hilang tanpa suara dan tidak ada yang tahu. Dengan `left` kita masih bisa menghitung dan memperingatkan. Ini pola yang berlaku di mana saja: **jangan pernah membuang baris tanpa menghitungnya lebih dulu.**

### Load punya urutan yang tidak bisa ditawar

```python
bersih.to_sql("penjualan_bersih_py", mesin_dw, if_exists="replace", index=False)
dimensi = muat_dimensi(mesin_dw, mesin_sumber, bersih)   # DIMENSI DULU
fakta   = muat_fakta(mesin_dw, bersih, dimensi)          # BARU FAKTA
buat_indeks(mesin_dw)                                    # INDEKS PALING AKHIR
```

Dimensi dulu, karena kunci dimensi baru ada setelah baris dimensinya terbentuk, sedangkan tabel fakta membutuhkan kunci itu. Membalik urutan ini akan menghasilkan tabel fakta penuh kunci kosong.

Setiap dimensi juga mendapat satu baris berkunci `-1`:

```python
KUNCI_TIDAK_DIKETAHUI = -1
```

Itu sebabnya `dim_produk_py` berisi 9 baris (8 produk + 1 Tidak Diketahui) dan `dim_cabang_py` berisi 4. Perannya sama dengan baris "Tanpa Pelanggan" di Sesi 2: menyediakan tempat berlabuh supaya tidak ada baris fakta yang hilang hanya karena kuncinya tidak ketemu.

### Indeks dibuat paling akhir, dan itu bukan kebetulan

```python
"ALTER TABLE fact_penjualan_py "
"  ADD INDEX i_tanggal (tanggal_key), ADD INDEX i_produk (produk_key), "
"  ADD INDEX i_cabang (cabang_key),   ADD INDEX i_pelanggan (pelanggan_key)"
```

Tabel hasil `to_sql()` lahir tanpa indeks sama sekali. Tanpa langkah ini, query OLAP di Sesi 4 bisa berjalan berpuluh kali lebih lambat — dan bukan dugaan: itu benar-benar terjadi saat modul ini diuji, query yang seharusnya selesai dalam sedetik tersangkut lebih dari dua menit.

Indeks selalu dibuat **sesudah** data dimuat, bukan sebelumnya, karena memelihara indeks sambil menyisipkan ribuan baris jauh lebih lambat daripada membangunnya sekali di akhir.

### Titik periksa

| Pemeriksaan | Nilai benar |
| --- | --- |
| `fact_penjualan_py` | 560 baris |
| Omzet di tabel fakta | 20.784.000 |
| `dim_tanggal_py` | 365 |
| `dim_produk_py` / `dim_cabang_py` / `dim_pelanggan_py` | 9 / 4 / 41 |
| Gagal lookup tanggal, produk, cabang | 0, 0, 0 |
| Baris tanpa identitas pelanggan | 167 |
| Jumlah produk berbeda | 8 |
| Tanggal gagal dibaca | 0 |

Dua angka pertama itu intinya seluruh sesi: **560 baris dan omzet 20.784.000, sama persis dengan Sesi 1 yang memakai SQL.** Dua jalan yang sangat berbeda — satu lewat `INSERT ... SELECT`, satu lewat pandas — bertemu di angka yang identik.

Buktikan sendiri dengan satu query:

```sql
SELECT (SELECT SUM(total) FROM penjualan_bersih)   AS versi_sql,
       (SELECT SUM(total) FROM fact_penjualan_py)  AS versi_python;
```

Kalau kedua kolom berbeda, salah satu jalur melewatkan sebuah aturan. Mencari tahu aturan mana yang terlewat adalah latihan debugging terbaik di seluruh praktikum ini.

## Sesi 4 — Query OLAP dan Data Mart

Sesi penutup memanen apa yang dibangun tiga sesi sebelumnya. Lima operasi OLAP dari Minggu 13, masing-masing satu query, semuanya di atas satu view.

```sql
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
```

View ini sendiri adalah pelajarannya: join berempat ditulis **sekali**, lalu delapan query berikutnya cukup `FROM v_penjualan`. Inilah bentuk paling sederhana dari data mart — lapisan yang menyembunyikan kerumitan skema bintang dari orang yang cuma ingin tahu angka penjualan.

### Lima operasi, lima query pendek

| Operasi | Artinya | Di query |
| --- | --- | --- |
| Roll-up | naik ke tingkat lebih ringkas | `GROUP BY bulan`, lalu `GROUP BY kuartal` |
| Drill-down | turun ke tingkat lebih rinci | kategori → `WHERE kategori = 'Kue'` per produk |
| Slice | memotong **satu** dimensi | `WHERE bulan = 2` |
| Dice | memotong **beberapa** dimensi | Kue + Cabang Pusat + akhir pekan |
| Pivot | memutar baris jadi kolom | `SUM(CASE WHEN bulan = 1 THEN total END)` |

Kelima istilah ini sering dihafal tanpa pernah dituliskan. Setelah sesi ini kamu tahu bahwa roll-up hanyalah `GROUP BY` di tingkat yang lebih tinggi, dan slice hanyalah `WHERE` — istilah besar untuk hal yang sudah kamu kuasai.

### Roll-up: dari harian naik ke bulanan, lalu ke kuartal

| bulan | hari | nota | potong | omzet |
| --- | --- | --- | --- | --- |
| Januari | 31 | 111 | 455 | 7.581.000 |
| Februari | 28 | 93 | 389 | 6.094.000 |
| Maret | 31 | 106 | 437 | 7.109.000 |
| **Kuartal 1** |  |  |  | **20.784.000** |

### Drill-down: kategori dulu, baru produk

Kue 13.801.000, Roti 5.166.000, Donat 1.817.000. Lalu turun ke dalam Kue:

| Produk | Potong | Omzet |
| --- | --- | --- |
| Lapis Legit | 123 | 5.535.000 |
| Brownies | 174 | 4.350.000 |
| Bolu Pandan | 178 | 3.916.000 |

Baca tabel itu dua kali. Bolu Pandan terjual **paling banyak** (178 potong) tapi menyumbang omzet **paling sedikit** di kategorinya. Lapis Legit terjual paling sedikit tapi menyumbang paling besar. Inilah gunanya drill-down: angka kategori yang rapi menyembunyikan dua cerita yang berlawanan, dan keputusan toko — produk mana yang dipromosikan — bergantung pada cerita mana yang dilihat.

### Pivot: bulan berpindah dari baris ke kolom

| Cabang | Januari | Februari | Maret | Kuartal 1 |
| --- | --- | --- | --- | --- |
| Cabang Pusat | 3.177.000 | 2.584.000 | 3.474.000 | 9.235.000 |
| Cabang Barat | 2.559.000 | 1.770.000 | 1.645.000 | 5.974.000 |
| Cabang Timur | 1.845.000 | 1.740.000 | 1.990.000 | 5.575.000 |

Bentuk ini yang diminta manajer, dan bentuk ini juga yang langsung bisa ditempel ke Excel. Cabang Barat turun tiga bulan berturut-turut sementara dua cabang lain naik di Maret — pola yang sama sekali tidak terlihat di tabel roll-up sebelumnya.

### Dua pembantu yang menghemat banyak pekerjaan

```sql
SELECT COALESCE(nama_cabang, 'SEMUA CABANG') AS cabang,
       COALESCE(kategori, 'semua kategori')  AS kategori,
       SUM(total) AS omzet
FROM v_penjualan
GROUP BY nama_cabang, kategori WITH ROLLUP;
```

`WITH ROLLUP` menghasilkan subtotal per cabang **dan** total keseluruhan dalam satu query. Tanpanya, pekerjaan ini biasanya dipecah jadi tiga query terpisah lalu dijumlahkan manual — dan di situlah salah hitung masuk. Baris terakhirnya: `SEMUA CABANG / semua kategori / 20.784.000`, angka yang sama yang sudah kita lihat di tiga sesi sebelumnya.

```sql
SELECT nama_cabang, peringkat, nama_produk, omzet
FROM (
  SELECT nama_cabang, nama_produk, omzet,
         RANK() OVER (PARTITION BY nama_cabang ORDER BY omzet DESC) AS peringkat
  FROM ( SELECT nama_cabang, nama_produk, SUM(total) AS omzet
         FROM v_penjualan GROUP BY nama_cabang, nama_produk ) x
) y
WHERE peringkat <= 2
ORDER BY nama_cabang, peringkat;
```

Fungsi window menjawab "dua produk terlaris di **setiap** cabang" — pertanyaan yang tidak bisa dijawab `GROUP BY` biasa. Hasilnya: Lapis Legit nomor satu di Pusat dan Timur, tapi di Barat kalah oleh Bolu Pandan.

Catat pola teknisnya, karena di titik inilah kebanyakan orang tersandung: MySQL tidak punya `QUALIFY`, jadi hasil `RANK()` harus dibungkus subquery dulu baru disaring di `WHERE`. Menulis `WHERE RANK() OVER (...) <= 2` langsung akan ditolak.

### Data mart sebagai penutup

```sql
CREATE OR REPLACE VIEW mart_bulanan AS
SELECT bulan, nama_bulan, nama_cabang, kategori,
       COUNT(DISTINCT no_nota) AS jumlah_nota,
       SUM(jumlah)             AS potong,
       SUM(total)              AS omzet
FROM v_penjualan
GROUP BY bulan, nama_bulan, nama_cabang, kategori;
```

Sesi berakhir di tempat Sesi 1 dimulai: lapisan penyajian. Bedanya sekarang kamu sudah menempuh seluruh jalannya sendiri, dari nota kasir sampai angka yang siap dibaca pemilik toko.

### Titik periksa

| Pemeriksaan | Nilai benar |
| --- | --- |
| Omzet Januari / Februari / Maret | 7.581.000 / 6.094.000 / 7.109.000 |
| Omzet per kategori (Kue / Roti / Donat) | 13.801.000 / 5.166.000 / 1.817.000 |
| Slice Februari, nota per cabang (Pusat / Barat / Timur) | 39 / 30 / 24 |
| Pivot, kuartal per cabang (Pusat / Barat / Timur) | 9.235.000 / 5.974.000 / 5.575.000 |
| Total `WITH ROLLUP` | 20.784.000 |
| Omzet berjalan Januari → Maret | 7.581.000 → 13.675.000 → 20.784.000 |

## Penilaian dan Kaitan ke Skripsi

### Pembagian bobot

| Sesi | Bobot | Yang harus kamu tunjukkan |
| --- | --- | --- |
| Sesi 1 | 25% | ketiga lapis berdiri, 560 baris, 8 nama produk, laporan pembersihan |
| Sesi 2 | 25% | grain tertulis, skema bintang jalan, jebakan non-additive dijawab |
| Sesi 3 | 30% | ETL jalan, log pembersihan lengkap, angka sama dengan Sesi 1 |
| Sesi 4 | 20% | lima operasi OLAP jalan, satu temuan bisnis ditulis |

Sesi 3 diberi bobot terbesar karena di sanalah seluruh rantai diuji: kalau Sesi 1 atau 2 dikerjakan setengah-setengah, angka Sesi 3 tidak akan cocok dan itu langsung terlihat.

### Satu syarat lulus yang tidak bisa ditawar

Angka **560 baris** dan **omzet 20.784.000** harus muncul di Sesi 1, Sesi 2, dan Sesi 3. Laporan yang menampilkan tiga angka berbeda berarti praktikum belum selesai, sebagus apa pun tampilannya.

Ini juga cara memeriksa pekerjaanmu paling cepat: buka laporan, cari tiga angka itu. Kalau cocok, rantai kerjanya utuh.

### Periksa pemahamanmu di akhir sesi

Empat pertanyaan, satu per sesi. Jawab tanpa membuka kode — pemahaman ini tidak bisa diperoleh dengan menyalin:

1. **Sesi 1** — Mengapa kolom di tabel staging bertipe `VARCHAR` semua, padahal kita tahu `jumlah` itu angka? *(Jawaban yang dicari: supaya satu baris rusak tidak menolak seluruh muatan; tipe data ditegakkan di lapis gudang.)*
2. **Sesi 2** — Mengapa `dim_tanggal` berisi 365 baris padahal transaksi cuma ada di 90 hari? *(Supaya hari tanpa penjualan tetap bisa dilaporkan — 275 hari itu baru bisa dihitung karena dimensinya lengkap.)*
3. **Sesi 3** — Mengapa dimensi harus dimuat sebelum tabel fakta? *(Kunci dimensi baru ada setelah barisnya terbentuk, dan tabel fakta butuh kunci itu.)*
4. **Sesi 4** — Bolu Pandan terjual paling banyak tapi omzetnya paling kecil di kategorinya. Apa artinya untuk pemilik toko? *(Pertanyaan ini menguji kemampuan membaca angka, bukan sekadar menghasilkannya.)*

Pertanyaan nomor 4 yang paling menentukan. Menjalankan kode itu bagian yang mudah; yang sering terlewat adalah menafsirkan hasilnya — padahal itu persis yang diminta di bab pembahasan skripsi.

### Dari praktikum ke skripsi

| Bagian skripsi | Dari sesi | Bentuk konkretnya |
| --- | --- | --- |
| Bab 3 — Analisis sistem berjalan | Sesi 1 | pemetaan sumber data dan bentuknya |
| Bab 3 — Perancangan | Sesi 1, 2 | gambar arsitektur tiga lapis + skema bintang |
| Bab 4 — Implementasi | Sesi 3 | skrip ETL dengan log pembersihan |
| Bab 4 — Pengujian | Sesi 1–3 | tabel verifikasi: dua jalur, satu angka |
| Bab 4 — Hasil dan pembahasan | Sesi 4 | tabel OLAP + temuan bisnis |

Empat sesi ini sudah membentuk satu kerangka skripsi yang utuh: ada sumber, ada rancangan, ada implementasi, ada pengujian, ada temuan. Yang perlu kamu ganti hanya studi kasusnya — koperasi, klinik, UMKM, apa pun yang punya data transaksi.

### Yang belum kamu pelajari di paket ini

Empat topik berikut tidak dipraktikkan di paket ini:

| Topik | Masih diajarkan? |
| --- | --- |
| Surrogate key dan SCD tipe 1/2 | dibahas di kuliah Minggu 6, tidak dipraktikkan |
| Incremental load dan watermark | dibahas di kuliah Minggu 10, tidak dipraktikkan |
| Visualisasi dan dashboard | tidak ada praktikumnya |
| Data mining: Apriori, RFM, peramalan | tidak ada praktikumnya |

Untuk kamu yang mengambil topik skripsi gudang data, paket 8 sesi lengkapnya tersedia dan bisa dikerjakan mandiri — khususnya sesi SCD dan incremental load, dua topik yang hampir selalu ditanyakan di sidang.

## Berkas, Urutan Jalan, dan Angka Kunci

### Isi folder

```
praktikum-dw-inti/
├── README.md                      panduan ringkas
├── konfigurasi.py                 satu-satunya berkas yang perlu diubah
├── cek_pemasangan.py              pemeriksa kesiapan laptop
├── requirements.txt               tiga pustaka Python
├── jalankan_semua.sh              menjalankan 4 sesi sekaligus dari nol
├── data/
│   ├── generate_data.py           pembuat data sumber (dijalankan sekali)
│   ├── seed_sumber.sql            transaksi Cabang Pusat & Timur
│   └── penjualan_barat.csv        ekspor Excel Cabang Barat (sengaja berantakan)
├── sesi1_arsitektur_tiga_lapis/   4 berkas SQL
├── sesi2_skema_bintang/           3 berkas SQL
├── sesi3_etl_python/              etl.py
├── sesi4_query_olap/              olap.sql
└── keluaran/                      hasil CSV (dibuat otomatis)
```

Seluruh paket di bawah 100 KB sebelum data dibuat, dan di bawah 10 MB sesudah gudang terisi.

### Urutan menjalankan dari nol

Semua perintah dijalankan **dari folder `praktikum-dw-inti`**, bukan dari dalam folder sesi.

```bash
# Persiapan sekali saja
python data/generate_data.py

# Sesi 1
mysql -u root -p                  < sesi1_arsitektur_tiga_lapis/01_buat_lapisan.sql
mysql -u root -p sumber_kasir     < data/seed_sumber.sql
mysql -u root -p --local-infile=1 < sesi1_arsitektur_tiga_lapis/03_staging.sql
mysql -u root -p                  < sesi1_arsitektur_tiga_lapis/04_gudang_dan_mart.sql
mysql -u root -p -t               < sesi1_arsitektur_tiga_lapis/05_verifikasi.sql

# Sesi 2
mysql -u root -p -t < sesi2_skema_bintang/01_dimensi.sql
mysql -u root -p -t < sesi2_skema_bintang/02_fakta.sql
mysql -u root -p -t < sesi2_skema_bintang/03_verifikasi.sql

# Sesi 3
python sesi3_etl_python/etl.py

# Sesi 4
mysql -u root -p -t < sesi4_query_olap/olap.sql
```

Untuk menjalankan ulang seluruh rangkaian dari nol dalam satu perintah:

```bash
chmod +x jalankan_semua.sh
DW_USER=root DW_PASS=sandimu ./jalankan_semua.sh
```

Seluruh rangkaian ini sudah dijalankan utuh dari nol di lingkungan MariaDB 10.11 dan berakhir bersih. Setiap angka di dokumen ini diambil dari jalannya, bukan dari perkiraan.

### Tabel angka kunci

Seed acaknya tetap, jadi kamu **harus** mendapat angka yang persis sama. Berbeda satu saja berarti ada langkah yang terlewat.

| Titik periksa | Nilai benar |
| --- | --- |
| `stg_penjualan_kasir` | 389 |
| `stg_penjualan_barat` | 188 |
| `penjualan_bersih` (Sesi 1) | 560 |
| dari kasir / dari Excel | 389 / 171 |
| Jumlah nota | 310 |
| Produk berbeda | 8 |
| Omzet satu kuartal | 20.784.000 |
| `dim_tanggal` (Sesi 2) | 365 |
| `fact_penjualan` (Sesi 2) | 560 |
| Hari tanpa penjualan | 275 |
| `fact_penjualan_py` (Sesi 3) | 560 |
| Omzet versi Python | 20.784.000 |
| Omzet Jan / Feb / Mar (Sesi 4) | 7.581.000 / 6.094.000 / 7.109.000 |
| Total `WITH ROLLUP` | 20.784.000 |

### Kalau tersendat

| Gejala | Sebabnya | Perbaikannya |
| --- | --- | --- |
| `LOAD DATA LOCAL INFILE` ditolak | klien tidak mengizinkan | jalankan dengan `--local-infile=1`, atau `SET GLOBAL local_infile=1;` |
| `File 'data/penjualan_barat.csv' not found` | folder kerja salah | kembali ke folder `praktikum-dw-inti` |
| `Access denied for user` | sandi kosong atau autentikasi soket | isi `DB_PASS`, atau buat pengguna khusus `CREATE USER 'dw'@'%' IDENTIFIED BY 'dw';` |
| Query Sesi 4 lambat sekali | indeks belum terbentuk | jalankan ulang `sesi3_etl_python/etl.py` |
| Angka tidak cocok tabel di atas | ada langkah terlewat | `DROP DATABASE` ketiganya, mulai dari awal |

Baris terakhir itu yang paling sering dipakai. Mengulang dari nol hanya butuh dua menit di paket sekecil ini — salah satu keuntungan nyata dari memperkecil data menjadi ratusan baris.
