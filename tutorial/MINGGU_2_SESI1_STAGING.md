# Tutorial Minggu 2 — Sesi 1: Tiga Database dan Staging

**Tujuan:** membangun tiga database (sumber, staging, gudang), mengisi sumber, lalu menyalin kedua sumber ke staging **apa adanya**.
**Target:** `stg_penjualan_kasir` = **389** baris dan `stg_penjualan_barat` = **188** baris.
**Waktu:** sekitar 30–45 menit.
**Bahan:** `modul-pdf/03_Sesi_1_...pdf` (atau `MODUL.md`), Langkah 1–3.

Syarat: tutorial [Minggu 1](MINGGU_1_PERSIAPAN.md) selesai dan `cek_pemasangan.py` lolos.

## Aturan penting sebelum mulai

1. **Semua perintah dijalankan dari folder utama repo**, bukan dari dalam folder sesi.
2. Perintah `mysql -u root -p` akan meminta sandi `root`. Di **Codespaces**, ganti dengan `mariadb` saja tanpa `-u` dan `-p`.
3. Tanda `<` adalah pengalihan masukan. **PowerShell di Windows tidak mendukungnya.** Di Windows, pakai **Git Bash**, atau **Command Prompt** (tulis jalur dengan `\`, misalnya `sesi1_arsitektur_tiga_lapis\01_buat_lapisan.sql`), atau pakai Codespaces.

## Gambaran: apa yang sedang dibangun

| Lapis | Database | Isinya |
| --- | --- | --- |
| Sumber | `sumber_kasir` | tabel rapi dari aplikasi kasir (cabang, produk, pelanggan, nota, nota_item) |
| Staging | `staging_toko` | salinan mentah kedua sumber |
| Gudang + mart | `dw_toko` | diisi minggu depan |

Ada dua sumber data: database kasir (Cabang Pusat dan Timur, rapi) dan ekspor Excel Cabang Barat (`data/penjualan_barat.csv`, sengaja berantakan).

## Langkah 1 — Buat tiga database

Pastikan data sumber sudah dibuat (dari Minggu 1; kalau belum, jalankan `python data/generate_data.py`).

```bash
mysql -u root -p < sesi1_arsitektur_tiga_lapis/01_buat_lapisan.sql
```

Berkas itu membuat `sumber_kasir`, `staging_toko`, dan `dw_toko`. Periksa:

```bash
mysql -u root -p -e "SHOW DATABASES;"
```

Ketiga nama itu harus muncul. Pikirkan: mengapa gudang dipisah dari sumber? (Jawabannya terasa minggu depan, saat pembersihan berjalan berat tapi aplikasi kasir tidak terganggu.)

## Langkah 2 — Isi database sumber

```bash
mysql -u root -p sumber_kasir < data/seed_sumber.sql
```

Periksa isinya:

```bash
mysql -u root -p -t -e "SELECT COUNT(*) AS nota FROM sumber_kasir.nota; SELECT * FROM sumber_kasir.produk;"
```

Kamu akan melihat daftar produk resmi. Ingat tabel ini: minggu depan dipakai untuk menyeragamkan nama produk dari Excel.

Lihat juga betapa berantakannya data Excel (buka `data/penjualan_barat.csv` di editor teks atau Excel). Perhatikan:
- tanggal berbentuk `30/01/2026`,
- nama produk kadang `ROTI KEJU`, kadang `roti keju`, kadang ada spasi di pinggir,
- ada baris yang sama dua kali,
- ada baris yang jumlahnya kosong.

## Langkah 3 — Salin ke staging

```bash
mysql -u root -p --local-infile=1 < sesi1_arsitektur_tiga_lapis/03_staging.sql
```

`--local-infile=1` wajib ada, karena berkas memakai `LOAD DATA LOCAL INFILE` untuk membaca CSV.

**Aturan staging: salin, jangan perbaiki.** Di tabel `stg_penjualan_barat`, semua kolom bertipe `VARCHAR`, termasuk `jumlah` dan `tanggal`. Itu disengaja. Di lapis ini kita belum tahu isinya bersih atau tidak, jadi satu baris rusak tidak boleh menolak seluruh muatan. Tipe data yang benar ditegakkan di lapis gudang.

## Titik periksa

```bash
mysql -u root -p -t -e "SELECT COUNT(*) AS kasir FROM staging_toko.stg_penjualan_kasir; SELECT COUNT(*) AS barat FROM staging_toko.stg_penjualan_barat;"
```

| Pemeriksaan | Nilai benar |
| --- | --- |
| `stg_penjualan_kasir` | 389 |
| `stg_penjualan_barat` | 188 |

## Kalau tersendat

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| `LOAD DATA LOCAL INFILE` ditolak | klien tidak mengizinkan | pakai `--local-infile=1`, atau jalankan `SET GLOBAL local_infile=1;` sebagai root |
| `File 'data/penjualan_barat.csv' not found` | folder kerja salah | `cd` ke folder utama repo |
| Ingin mengulang dari awal | salah langkah | jalankan ulang Langkah 1: berkas itu menghapus dan membuat ulang ketiga database, lalu lanjut Langkah 2 dan 3 |
| Angka tidak 389 / 188 | langkah terlewat | ulangi dari Langkah 1; hanya butuh dua menit |
| `Access denied` | sandi salah | cek sandi root; di Codespaces pakai `mariadb` |

Untuk mengulang dari nol, cukup jalankan Langkah 1 lagi (ia menghapus dan membuat ulang ketiga database), lalu Langkah 2 dan 3. Jangan lupa Langkah 2, karena `sumber_kasir` ikut terhapus.

## Yang dikumpulkan ke LMS

1. **Screenshot:** hasil `COUNT(*)` untuk dua tabel staging (389 dan 188).
2. **Jawaban:** mengapa staging hanya menyalin data apa adanya tanpa memperbaikinya? (1–3 kalimat)
3. **Opsional:** satu hal yang masih membingungkanmu.

Minggu depan: membersihkan data dan memuatnya ke gudang.
