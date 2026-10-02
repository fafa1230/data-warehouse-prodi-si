# Tutorial Minggu 7 — Sesi 4: Query OLAP dan Data Mart

**Tujuan:** menjalankan lima operasi OLAP di atas gudang data yang sudah kamu bangun.
**Target:** omzet Januari / Februari / Maret = **7.581.000 / 6.094.000 / 7.109.000** dan total `WITH ROLLUP` = **20.784.000**.
**Waktu:** sekitar 45 menit.
**Bahan:** `modul-pdf/06_Sesi_4_Query_OLAP_dan_Data_Mart.pdf`.

Syarat: Minggu 6 selesai (tabel `*_py` ada di `dw_toko`, termasuk indeksnya).

## Gambaran

Sesi ini memanen apa yang dibangun tiga sesi sebelumnya. Semua query berjalan di atas satu **view**:

```sql
CREATE OR REPLACE VIEW v_penjualan AS
SELECT ... FROM fact_penjualan_py f
JOIN dim_tanggal_py t ON ... JOIN dim_produk_py p ON ...
JOIN dim_cabang_py c ON ... JOIN dim_pelanggan_py pl ON ...;
```

Join berempat ditulis **sekali**, lalu semua query berikutnya cukup `FROM v_penjualan`. Itulah bentuk paling sederhana dari data mart: lapisan yang menyembunyikan kerumitan skema bintang dari orang yang hanya ingin tahu angka penjualan.

## Langkah 1 — Jalankan semua query

```bash
mysql -u root -p -t < sesi4_query_olap/olap.sql
```

Keluarannya panjang. Simpan ke berkas agar mudah dibaca ulang:

```bash
mysql -u root -p -t < sesi4_query_olap/olap.sql > keluaran/hasil_olap.txt
```

(Folder `keluaran/` tidak ikut ke GitHub, jadi aman.) Buka berkas itu bersama `sesi4_query_olap/olap.sql` dan cocokkan tiap hasil dengan querynya.

## Langkah 2 — Kenali lima operasi

| Operasi | Artinya | Di query |
| --- | --- | --- |
| **Roll-up** | naik ke tingkat lebih ringkas | `GROUP BY bulan`, lalu `GROUP BY kuartal` |
| **Drill-down** | turun ke tingkat lebih rinci | kategori, lalu `WHERE kategori = 'Kue'` per produk |
| **Slice** | memotong **satu** dimensi | `WHERE bulan = 2` |
| **Dice** | memotong **beberapa** dimensi | Kue + Cabang Pusat + akhir pekan |
| **Pivot** | memutar baris jadi kolom | `SUM(CASE WHEN bulan = 1 THEN total END)` |

Istilah besar, tetapi roll-up hanyalah `GROUP BY` di tingkat lebih tinggi dan slice hanyalah `WHERE`.

## Langkah 3 — Cocokkan hasilnya

**Roll-up (per bulan)**

| Bulan | Omzet |
| --- | --- |
| Januari | 7.581.000 |
| Februari | 6.094.000 |
| Maret | 7.109.000 |
| Kuartal 1 | 20.784.000 |

**Drill-down: kategori, lalu produk dalam Kue**

Kue 13.801.000, Roti 5.166.000, Donat 1.817.000. Di dalam Kue:

| Produk | Potong | Omzet |
| --- | --- | --- |
| Lapis Legit | 123 | 5.535.000 |
| Brownies | 174 | 4.350.000 |
| Bolu Pandan | 178 | 3.916.000 |

**Pivot: omzet per cabang per bulan**

| Cabang | Januari | Februari | Maret | Kuartal 1 |
| --- | --- | --- | --- | --- |
| Cabang Pusat | 3.177.000 | 2.584.000 | 3.474.000 | 9.235.000 |
| Cabang Barat | 2.559.000 | 1.770.000 | 1.645.000 | 5.974.000 |
| Cabang Timur | 1.845.000 | 1.740.000 | 1.990.000 | 5.575.000 |

**Titik periksa lainnya**

| Pemeriksaan | Nilai benar |
| --- | --- |
| Slice Februari, nota per cabang (Pusat / Barat / Timur) | 39 / 30 / 24 |
| Total `WITH ROLLUP` | 20.784.000 |
| Omzet berjalan Januari → Maret | 7.581.000 → 13.675.000 → 20.784.000 |

## Langkah 4 — Dua query lanjutan

**`WITH ROLLUP`** menghasilkan subtotal per cabang **dan** total keseluruhan dalam satu query. Baris terakhirnya `SEMUA CABANG / semua kategori / 20.784.000`, angka yang sama dengan tiga sesi sebelumnya.

**Fungsi window `RANK()`** menjawab "dua produk terlaris di **setiap** cabang". Catat jebakan teknisnya: MySQL tidak punya `QUALIFY`, jadi hasil `RANK()` harus dibungkus subquery dulu, baru disaring di `WHERE`. Menulis `WHERE RANK() OVER (...) <= 2` langsung akan ditolak.

## Langkah 5 — Bacalah angkanya, jangan hanya menjalankannya

Menjalankan query itu mudah. Yang sering terlewat adalah **menafsirkan hasilnya**. Latihannya:

- Di tabel drill-down, **Bolu Pandan terjual paling banyak (178 potong) tetapi omzetnya paling kecil di kategorinya**, sedangkan Lapis Legit terjual paling sedikit tetapi omzetnya paling besar. Apa artinya bagi pemilik toko yang menentukan produk mana yang dipromosikan?
- Di tabel pivot, Cabang Barat turun tiga bulan berturut-turut, sementara dua cabang lain naik di Maret. Pola ini tidak terlihat di tabel roll-up.

Pilih **satu temuan** seperti ini, dan tulis dalam 2–3 kalimat. Itu yang dinilai di Sesi 4 dan menjadi latihan untuk bab pembahasan skripsimu.

## Kalau tersendat

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Query sangat lambat (menit, bukan detik) | indeks belum terbentuk | jalankan ulang `python sesi3_etl_python/etl.py` sampai selesai |
| `Table 'fact_penjualan_py' doesn't exist` | `etl.py` belum dijalankan penuh | selesaikan Minggu 5–6 |
| Angka tidak cocok | ada langkah Sesi 1–3 yang terlewat | ulangi dari Minggu 2; total harus 20.784.000 |
| Error pada `RANK()` | versi MySQL terlalu lama | pakai MariaDB 10.4+ atau MySQL 8 |

## Yang dikumpulkan ke LMS

1. **Screenshot:** omzet Januari / Februari / Maret dan total `WITH ROLLUP` (20.784.000).
2. **Jawaban:** bedakan roll-up dan drill-down dengan satu contoh dari data praktikum. (1–3 kalimat)
3. **Temuan bisnis:** satu temuan dari hasil OLAP, 2–3 kalimat.
4. **Opsional:** satu hal yang masih membingungkanmu.

Minggu depan: penutup dan kaitan ke skripsi.
