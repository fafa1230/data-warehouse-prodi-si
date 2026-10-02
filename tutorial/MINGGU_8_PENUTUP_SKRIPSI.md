# Tutorial Minggu 8 — Penutup dan Kaitan ke Skripsi

**Tujuan:** merangkum seluruh praktikum, memeriksa pemahamanmu, dan menghubungkannya ke skripsi.
**Target:** menjawab empat pertanyaan pemahaman tanpa membuka kode, dan menulis ringkasan satu halaman.
**Waktu:** sekitar 60 menit (tidak ada kode baru).
**Bahan:** `modul-pdf/07_Penilaian_dan_Kaitan_ke_Skripsi.pdf` dan `08_Berkas_Urutan_Jalan_dan_Angka_Kunci.pdf`.

## Langkah 1 — Periksa rantai kerjamu

Tiga angka ini harus muncul di laporanmu, dan harus **sama di Sesi 1, 2, dan 3**:

| Angka | Sesi 1 | Sesi 2 | Sesi 3 |
| --- | --- | --- | --- |
| Jumlah baris | `penjualan_bersih` = 560 | `fact_penjualan` = 560 | `fact_penjualan_py` = 560 |
| Omzet | 20.784.000 | 20.784.000 | 20.784.000 |

Laporan yang menampilkan angka berbeda berarti praktikum belum selesai, sebagus apa pun tampilannya. Ini juga cara memeriksa pekerjaanmu paling cepat.

Kalau ada yang tidak cocok, jalankan pembanding dari nol:

```bash
chmod +x jalankan_semua.sh
DW_USER=root DW_PASS=sandimu ./jalankan_semua.sh
```

Skrip ini menjalankan keempat sesi berurutan dari nol, sehingga bisa dipakai sebagai pembanding hasilmu. Saat belajar, kerjakan langkah satu per satu, bukan lewat skrip ini. (Di Windows, jalankan lewat Git Bash atau Codespaces. Skrip ini memakai `mariadb` secara bawaan; kalau klienmu bernama `mysql`, atur `DW_CLIENT=mysql`.)

## Langkah 2 — Pahami pembagian bobot penilaian

| Sesi | Bobot | Yang harus kamu tunjukkan |
| --- | --- | --- |
| Sesi 1 | 25% | ketiga lapis berdiri, 560 baris, 8 nama produk, laporan pembersihan |
| Sesi 2 | 25% | grain tertulis, skema bintang jalan, jebakan non-additive dijawab |
| Sesi 3 | 30% | ETL jalan, log pembersihan lengkap, angka sama dengan Sesi 1 |
| Sesi 4 | 20% | lima operasi OLAP jalan, satu temuan bisnis ditulis |

Pembagian bobot di atas adalah rancangan modul. Bobot per minggu di LMS dan komponen penilaian akhir mengikuti pengumuman dosen.

## Langkah 3 — Jawab empat pertanyaan pemahaman

Jawab **tanpa membuka kode**. Pemahaman ini tidak bisa diperoleh dengan menyalin.

1. **Sesi 1:** mengapa kolom di tabel staging bertipe `VARCHAR` semua, padahal kita tahu `jumlah` itu angka?
2. **Sesi 2:** mengapa `dim_tanggal` berisi 365 baris padahal transaksi cuma ada di 90 hari?
3. **Sesi 3:** mengapa dimensi harus dimuat sebelum tabel fakta?
4. **Sesi 4:** Bolu Pandan terjual paling banyak tetapi omzetnya paling kecil di kategorinya. Apa artinya untuk pemilik toko?

Nomor 4 paling menentukan. Menjalankan kode itu bagian yang mudah; yang sering terlewat adalah menafsirkan hasilnya.

## Langkah 4 — Hubungkan ke skripsi

Empat sesi ini membentuk satu kerangka skripsi yang utuh:

| Bagian skripsi | Dari sesi | Bentuk konkretnya |
| --- | --- | --- |
| Bab 3 — Analisis sistem berjalan | Sesi 1 | pemetaan sumber data dan bentuknya |
| Bab 3 — Perancangan | Sesi 1, 2 | gambar arsitektur tiga lapis dan skema bintang |
| Bab 4 — Implementasi | Sesi 3 | skrip ETL dengan log pembersihan |
| Bab 4 — Pengujian | Sesi 1–3 | tabel verifikasi: dua jalur, satu angka |
| Bab 4 — Hasil dan pembahasan | Sesi 4 | tabel OLAP dan temuan bisnis |

Yang perlu diganti hanya studi kasusnya: koperasi, klinik, UMKM, atau apa pun yang punya data transaksi.

Jawab dua hal ini dalam ringkasanmu:

1. **Pada topik skripsimu** (atau topik yang sedang kamu pertimbangkan), data transaksi apa yang akan dijadikan gudang data? Apa grain-nya (satu baris tabel fakta mewakili apa)? Dimensi apa saja yang kamu butuhkan?
2. **Apa yang belum dicakup** praktikum ini? Pilih satu dari tabel di bawah, dan jelaskan mengapa itu relevan untuk topikmu.

| Topik yang belum dipraktikkan | Keterangan |
| --- | --- |
| Surrogate key dan SCD tipe 1/2 | dibahas di kuliah, tidak dipraktikkan |
| Incremental load dan watermark | dibahas di kuliah, tidak dipraktikkan |
| Visualisasi dan dashboard | tidak ada praktikumnya |
| Data mining: Apriori, RFM, peramalan | tidak ada praktikumnya |

## Yang dikumpulkan ke LMS

Satu halaman ringkasan (tanpa screenshot), berisi:

1. Jawaban empat pertanyaan di Langkah 3 (masing-masing 1–3 kalimat).
2. Jawaban dua hal di Langkah 4: rancangan singkat untuk topik skripsimu, dan satu topik yang belum dicakup beserta alasannya.
3. **Opsional:** satu hal yang masih membingungkanmu.

Penilaian minggu ini dilihat dari **kejelasan keterkaitan** antara praktikum dan topikmu, bukan dari kecocokan dengan satu jawaban baku.

Selamat, kamu sudah menempuh seluruh jalan dari nota kasir sampai angka yang siap dibaca pemilik toko.
