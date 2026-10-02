# Tutorial Minggu 5 — Sesi 3: ETL dengan Python (Extract dan Transform)

**Tujuan:** menjalankan skrip ETL dan **membaca** dua bagian pertamanya (Extract dan Transform), terutama log baris yang dibuang.
**Target:** skrip berjalan sampai selesai, dan log Transform terbaca: 188 → 183 → 171 baris untuk Excel, hasil akhir **560** baris.
**Waktu:** sekitar 30–45 menit.
**Bahan:** `modul-pdf/05_Sesi_3_ETL_dengan_Python.pdf`, bagian Extract dan Transform.

Syarat: Sesi 1 selesai (database `sumber_kasir` dan `dw_toko` ada) dan variabel `DW_USER` / `DW_PASS` sudah diatur di terminal ini (lihat [Minggu 1](MINGGU_1_PERSIAPAN.md)).

## Gambaran

Sesi ini mengerjakan ulang pekerjaan Sesi 1, kali ini dengan Python. Satu berkas, `sesi3_etl_python/etl.py`, dengan tiga bagian yang diberi garis pemisah di kodenya:

| Bagian | Tugas |
| --- | --- |
| 1. EXTRACT | tarik apa adanya dari MySQL dan dari CSV |
| 2. TRANSFORM | bersihkan, seragamkan, catat yang dibuang |
| 3. LOAD | muat dimensi dulu, baru fakta, terakhir indeks (minggu depan) |

Berkas ini dijalankan **sekali dari awal sampai akhir**. Minggu ini kamu fokus membaca keluaran dan kode bagian 1–2. Bagian 3 dibahas minggu depan, tetapi ikut berjalan sekarang.

## Langkah 1 — Jalankan skrip

Dari folder utama repo:

```bash
python sesi3_etl_python/etl.py
```

(Di macOS/Linux, pakai `python3` bila `python` tidak dikenali.) Selesai dalam 1–3 detik.

Kalau muncul error koneksi, periksa `DW_USER` dan `DW_PASS` di terminal yang sama, lalu ulangi.

## Langkah 2 — Baca keluaran Bagian 1: Extract

Kamu akan melihat jumlah baris yang ditarik:

- dari database kasir: 389 baris,
- dari file Excel: 188 baris,
- tabel rujukan produk: 8 baris,

lalu lima baris pertama data Excel yang mentah dan berantakan.

Buka `etl.py` dan baca fungsi `extract_barat()`. Perhatikan `dtype=str`: data dibaca sebagai teks semua. Prinsipnya sama dengan kolom `VARCHAR` di staging Sesi 1, hanya alatnya yang berbeda. Alasannya: satu baris dengan jumlah kosong akan menggagalkan pembacaan seluruh file kalau pandas dipaksa menebak tipe angka.

**Extract hanya menarik, tidak membersihkan.** Makin cepat extract selesai, makin singkat sistem sumber terganggu.

## Langkah 3 — Baca keluaran Bagian 2: Transform

Kamu akan melihat tabel log seperti ini:

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

Cocokkan dengan hitunganmu minggu lalu: 188 − 5 − 12 = 171, lalu 389 + 171 = 560. Setelah tabel itu ada dua baris pemeriksaan: produk berbeda = 8, tanggal gagal dibaca = 0.

**Mengapa log ini penting?** ETL yang hanya mencetak "selesai" tidak bisa dipercaya. Yang bisa dipercaya adalah ETL yang bisa ditanya: *dari 188 baris, ke mana perginya 17?* Tabel di atas menjawabnya baris per baris. Kalau kamu memakai ETL di skripsi, pertanyaan ini hampir pasti muncul di sidang.

## Langkah 4 — Baca kode Transform

Buka fungsi `transform_barat()` dan cari bagian pencocokan nama produk:

```python
df = df.merge(produk[["kunci", "nama_produk", "kategori"]],
              on="kunci", how="left", suffixes=("_asli", ""))
tidak_cocok = int(df["nama_produk"].isna().sum())
if tidak_cocok:
    print(f"PERINGATAN: {tidak_cocok} baris tidak cocok ke tabel produk.")
```

Perhatikan `how="left"`, lalu baris yang tidak cocok dihitung. Kalau memakai `how="inner"`, baris yang gagal dicocokkan hilang **tanpa suara** dan tidak ada yang tahu. Pola ini berlaku di mana saja: **jangan pernah membuang baris tanpa menghitungnya lebih dulu.**

Cocokkan juga dengan Sesi 1: pencocokan nama memakai tabel `produk` resmi, bukan `.str.title()`.

## Langkah 5 — Lihat berkas hasil

Skrip menyimpan hasil Transform ke `keluaran/penjualan_bersih.csv`. Buka dan periksa: ada 560 baris data, kolom `sumber` berisi `kasir` atau `excel`.

(Folder `keluaran/` memang tidak ikut ke GitHub karena dibuat ulang tiap kali skrip berjalan.)

## Kalau tersendat

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| `ModuleNotFoundError: pandas` | pustaka belum terpasang | `pip install -r requirements.txt` |
| `Access denied for user` | sandi belum diatur di terminal ini | atur ulang `DW_PASS`, lalu jalankan lagi |
| `Unknown database 'sumber_kasir'` | Sesi 1 belum dikerjakan | selesaikan Minggu 2–3 |
| `FileNotFoundError ... penjualan_barat.csv` | folder kerja salah | `cd` ke folder utama repo |
| Angka tidak 560 | data sumber atau Sesi 1 tidak lengkap | ulangi Sesi 1, lalu jalankan lagi `etl.py` |

Skrip aman dijalankan berkali-kali, karena tabel hasilnya ditulis ulang (`if_exists="replace"`).

## Yang dikumpulkan ke LMS

1. **Screenshot:** tabel log Transform (langkah, masuk, dibuang, keluar) sampai baris HASIL AKHIR 560.
2. **Jawaban:** mengapa Extract hanya menarik data dan tidak membersihkannya? (1–3 kalimat)
3. **Opsional:** satu hal yang masih membingungkanmu.

Minggu depan: bagian Load, dan membuktikan bahwa Python dan SQL menghasilkan angka yang sama.
