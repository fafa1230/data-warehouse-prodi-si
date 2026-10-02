# Tutorial Minggu 4 — Sesi 2: Skema Bintang

**Tujuan:** mengubah tabel lebar `penjualan_bersih` menjadi satu tabel fakta dengan empat dimensi.
**Target:** `dim_tanggal` = **365**, `fact_penjualan` = **560**, hari tanpa penjualan = **275**.
**Waktu:** sekitar 30–45 menit.
**Bahan:** `modul-pdf/04_Sesi_2_Skema_Bintang.pdf`.

Syarat: Sesi 1 selesai (`penjualan_bersih` = 560).

## Konsep yang harus dipahami lebih dulu

**Grain** adalah arti satu baris di tabel fakta. Kalimat grain kita:

> Satu baris di `fact_penjualan` mewakili **penjualan satu produk pada satu nota**.

Kalimat ini ditetapkan **sebelum** menulis kolom apa pun, karena ia menentukan ukuran mana yang boleh dijumlahkan, dimensi mana yang perlu, dan query mana yang mustahil dijawab. Nota berisi tiga produk menghasilkan tiga baris.

Bentuk skemanya: satu tabel fakta di tengah, dikelilingi empat dimensi (tanggal, produk, cabang, pelanggan).

## Langkah 1 — Buat dimensi

```bash
mysql -u root -p -t < sesi2_skema_bintang/01_dimensi.sql
```

Hal yang perlu kamu perhatikan di berkas itu:

- **`dim_tanggal` dibuat sendiri untuk satu tahun penuh** (365 baris) memakai `WITH RECURSIVE`, padahal transaksi hanya ada di 90 hari. Itu disengaja: pertanyaan "hari apa toko tidak menjual apa pun?" baru bisa dijawab bila hari kosong punya baris di dimensi.
- **`dim_produk` punya kolom baru** yang tidak ada di sumber mana pun (kelas harga: Murah / Sedang / Mahal). Dimensi bukan salinan tabel sumber, melainkan tempat menaruh cara bisnis memandang sesuatu.
- **`dim_pelanggan` punya baris khusus berkunci 0**, "Tanpa Pelanggan". Ada 167 transaksi tanpa identitas pembeli. Kalau `NULL` dibiarkan, `INNER JOIN` menghapus 167 baris itu dan omzet meleset.

## Langkah 2 — Buat tabel fakta

```bash
mysql -u root -p -t < sesi2_skema_bintang/02_fakta.sql
```

Perhatikan dua hal di berkasnya:

- `COALESCE(id_pelanggan, 0)` mengarahkan transaksi tanpa identitas ke baris "Tanpa Pelanggan", bukan membuangnya.
- `no_nota` duduk di tabel fakta tanpa dimensi sendiri. Ini disebut **degenerate dimension**: tidak ada atribut lain yang bisa digantung padanya, jadi `dim_nota` hanya akan jadi tabel satu kolom.

Di komentar berkas itu, cari kolom `harga_satuan` yang ditandai **NON-additive**. Kita kembali ke ini di bawah.

## Langkah 3 — Verifikasi

```bash
mysql -u root -p -t < sesi2_skema_bintang/03_verifikasi.sql
```

| Pemeriksaan | Nilai benar |
| --- | --- |
| `dim_tanggal` / `dim_produk` / `dim_cabang` / `dim_pelanggan` | 365 / 8 / 3 / 41 |
| `fact_penjualan` | 560 baris, omzet 20.784.000 |
| Nota + produk kembar | 0 baris |
| Omzet per kategori (Kue / Roti / Donat) | 13.801.000 / 5.166.000 / 1.817.000 |
| Omzet per hari: akhir pekan vs hari kerja | 301.808 vs 202.141 |
| Hari tanpa penjualan | 275 |

`dim_pelanggan` berisi **41** baris, bukan 40: empat puluh pelanggan ditambah satu baris "Tanpa Pelanggan".

Omzet **20.784.000 harus sama persis** dengan Sesi 1. Memindahkan data ke skema bintang tidak boleh menambah atau mengurangi satu rupiah pun.

## Jebakan ukuran non-additive (wajib dipahami)

Blok pemeriksaan nomor 6 menampilkan tiga angka dari tabel yang sama:

| Cara menghitung | Hasil | Benar? |
| --- | --- | --- |
| `SUM(harga_satuan)` | 8.870.000 | tidak bermakna apa pun |
| `AVG(harga_satuan)` | 15.839 | salah, tiap baris dihitung sama bobotnya |
| `SUM(total) / SUM(jumlah)` | 16.225 | benar |

`jumlah` dan `total` **additive**: boleh dijumlahkan ke arah dimensi mana pun. `harga_satuan` **tidak**. Rata-rata tanpa bobot memberi roti murah yang terjual banyak pengaruh yang sama dengan lapis legit yang terjual sedikit. Selisih 15.839 melawan 16.225 kecil, dan justru itu berbahaya: angka salah yang kelihatan masuk akal lolos lebih sering daripada yang jelas ngawur.

## Kalau tersendat

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| `Table 'penjualan_bersih' doesn't exist` | Sesi 1 belum selesai | selesaikan Minggu 3 dulu |
| `fact_penjualan` bukan 560 | dimensi belum lengkap, atau `INNER JOIN` membuang baris | cek `dim_pelanggan` = 41 dan baris kunci 0 |
| `dim_tanggal` bukan 365 | `WITH RECURSIVE` tidak jalan | pakai MariaDB 10.4+ atau MySQL 8 |
| Ingin mengulang Sesi 2 | salah langkah | jalankan ulang `01_dimensi.sql`, `02_fakta.sql`, lalu `03_verifikasi.sql` (aman diulang, tabel lama dihapus otomatis) |

## Yang dikumpulkan ke LMS

1. **Screenshot:** jumlah baris `dim_tanggal` (365), `fact_penjualan` (560), dan hari tanpa penjualan (275).
2. **Jawaban:** apa itu grain tabel fakta, dan mengapa harus ditetapkan sebelum menulis kolom? (1–3 kalimat)
3. **Opsional:** satu hal yang masih membingungkanmu.

> Bobot penilaian Sesi 2 juga mencakup **kalimat grain yang tertulis** dan **jawaban jebakan non-additive**. Tulis keduanya dengan kata-katamu sendiri di laporan.

Minggu depan: ETL dengan Python.
