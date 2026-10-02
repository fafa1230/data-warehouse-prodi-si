# Jadwal Belajar Mandiri — 8 Minggu

Panduan ini untuk belajar sendiri dengan modul di repo ini. Tiap minggu ada
bahan yang dibaca, pekerjaan yang dilakukan, dan **target** yang harus tercapai
sebelum lanjut. Target selalu berupa angka kunci, jadi kamu bisa memeriksanya
sendiri tanpa menunggu dosen. Daftar angka kunci lengkap ada di
[README.md](README.md#angka-kunci-untuk-memeriksa-pekerjaanmu).

Kalau angkamu berbeda dari target, jangan lanjut. Ulangi dari awal dengan
`DROP DATABASE` pada ketiga database, lalu jalankan lagi. Mengulang hanya
butuh dua menit.

| Minggu | Topik | Bahan | Target |
| --- | --- | --- | --- |
| 1 | Persiapan | `modul-pdf/01` dan `02`, [tutorial minggu 1](tutorial/MINGGU_1_PERSIAPAN.md) | `python cek_pemasangan.py` lolos semua |
| 2 | Sesi 1, bagian awal | `modul-pdf/03`, Langkah 1–3, [tutorial](tutorial/MINGGU_2_SESI1_STAGING.md) | `stg_penjualan_kasir` = 389, `stg_penjualan_barat` = 188 |
| 3 | Sesi 1, bagian akhir | `modul-pdf/03`, Langkah 4–5, [tutorial](tutorial/MINGGU_3_SESI1_PEMBERSIHAN.md) | `penjualan_bersih` = 560 (389 kasir + 171 Excel), omzet = 20.784.000 |
| 4 | Sesi 2, skema bintang | `modul-pdf/04`, [tutorial](tutorial/MINGGU_4_SESI2_SKEMA_BINTANG.md) | `dim_tanggal` = 365, `fact_penjualan` = 560 |
| 5 | Sesi 3, extract dan transform | `modul-pdf/05`, bagian Extract dan Transform, [tutorial](tutorial/MINGGU_5_SESI3_EXTRACT_TRANSFORM.md) | Skrip berjalan sampai Transform, catatan baris yang dibuang terbaca |
| 6 | Sesi 3, load | `modul-pdf/05`, bagian Load, [tutorial](tutorial/MINGGU_6_SESI3_LOAD.md) | `fact_penjualan_py` = 560, omzet Python = 20.784.000 |
| 7 | Sesi 4, query OLAP | `modul-pdf/06`, [tutorial](tutorial/MINGGU_7_SESI4_OLAP.md) | Omzet Jan/Feb/Mar = 7.581.000 / 6.094.000 / 7.109.000, total `WITH ROLLUP` = 20.784.000 |
| 8 | Penutup | `modul-pdf/07` dan `08`, [tutorial](tutorial/MINGGU_8_PENUTUP_SKRIPSI.md) | Jawab pertanyaan pemahaman, rancang kaitan ke skripsimu |

## Cara mengerjakan tiap minggu

1. Baca bahan minggu itu dulu, jangan langsung menjalankan kode.
2. Jalankan perintahnya dari **folder utama repo**, urutannya ada di README.
3. Cocokkan angkamu dengan kolom Target. Kalau sama, lanjut. Kalau beda, ulangi.
4. Catat satu hal yang belum kamu pahami. Bawa ke dosen atau diskusi kelas.

## Catatan per minggu

- **Minggu 1.** Pilih salah satu: Codespaces (tanpa pasang apa pun), unduh ZIP,
  atau clone. Pakai Codespaces kalau RAM laptopmu di bawah 4 GB.
- **Minggu 2–3.** Inti Sesi 1: data mentah disalin apa adanya ke staging, lalu
  dibersihkan. Jangan memperbaiki data saat menyalin.
- **Minggu 4.** Tetapkan grain lebih dulu sebelum menulis kolom apa pun.
- **Minggu 5–6.** Sesi 3 mengerjakan ulang hasil Sesi 1 dengan Python. Kedua
  versi harus berhenti di angka yang sama: 560 baris dan omzet 20.784.000.
- **Minggu 7.** Lima operasi OLAP: roll-up, drill-down, slice, dice, pivot.
- **Minggu 8.** Lihat bobot penilaian dan syarat lulus di `modul-pdf/07`.

## Kalau tertinggal

Jangan lompat sesi, karena Sesi 1 sampai 4 berurutan. Kejar dengan
mengerjakan dua minggu sekaligus di akhir pekan. Jumlah barisnya kecil,
jadi tiap sesi selesai dalam hitungan menit setelah kamu paham alurnya.
