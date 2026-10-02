# Tutorial Minggu 3 — Sesi 1: Pembersihan dan Gudang

**Tujuan:** membersihkan data staging, menggabungkan dua sumber ke satu tabel gudang, lalu membuat data mart.
**Target:** `penjualan_bersih` = **560** baris (389 dari kasir + 171 dari Excel), 8 nama produk, omzet **20.784.000**.
**Waktu:** sekitar 30–45 menit.
**Bahan:** `modul-pdf/03_Sesi_1_...pdf`, Langkah 4–5.

Syarat: Minggu 2 selesai (staging berisi 389 dan 188 baris).

## Gambaran

Data Excel Cabang Barat masuk lewat empat aturan pembersihan:

| # | Masalah | Cara menanganinya | Efek |
| --- | --- | --- | --- |
| 1 | Tanggal `dd/mm/yyyy` bertipe teks | `STR_TO_DATE(..., '%d/%m/%Y')` | menjadi tipe `DATE` |
| 2 | Nama produk campur besar-kecil dan spasi | `JOIN` ke tabel `produk` resmi | nama selalu nama resmi |
| 3 | Baris tanpa jumlah | `WHERE TRIM(jumlah) <> ''` | 5 baris dibuang |
| 4 | Baris kembar | `DISTINCT` | 12 baris dibuang |

Hitung sendiri sebelum menjalankan: **188 − 5 − 12 = 171**.

Kenapa menyeragamkan nama lewat `JOIN` ke tabel produk, bukan mengubah huruf besar-kecil? Karena `Roti coklat` beda satu huruf dari `Roti Coklat`, dan satu produk akan terpecah jadi dua baris di laporan. Mencocokkan ke tabel resmi menutup celah itu.

## Langkah 4 — Muat ke gudang dan buat data mart

```bash
mysql -u root -p < sesi1_arsitektur_tiga_lapis/04_gudang_dan_mart.sql
```

Berkas ini:
- membuat tabel `penjualan_bersih` di `dw_toko`,
- memuat data kasir (sudah rapi, tinggal dihitung totalnya),
- memuat data Excel yang sudah dibersihkan,
- membuat dua view data mart.

Buka berkasnya dengan editor dan cari komentar `GRAIN`. Satu baris di tabel ini adalah satu produk pada satu nota.

Perhatikan kolom `sumber` (`kasir` atau `excel`). Kolom kecil ini menyelamatkan banyak waktu bila angka tidak cocok, karena langsung terlihat sumber mana yang bermasalah.

## Langkah 5 — Verifikasi

```bash
mysql -u root -p -t < sesi1_arsitektur_tiga_lapis/05_verifikasi.sql
```

Hasilnya tujuh blok pemeriksaan. Cocokkan dengan tabel ini:

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

**Titik periksa paling tajam: nama produk berbeda harus tepat 8.** Kalau muncul 9 atau lebih, pencocokan nama gagal dan ada produk yang terpecah.

## Kalau angkamu berbeda

| Angka | Kemungkinan sebab |
| --- | --- |
| Excel = 188, bukan 171 | `DISTINCT` terlewat dan filter jumlah kosong tidak jalan |
| Excel = 183 | filter jumlah kosong jalan, tapi duplikat belum dibuang |
| Nama produk berbeda lebih dari 8 | pencocokan nama ke tabel `produk` gagal |
| Tabel `penjualan_bersih` kosong | staging belum terisi (ulangi Minggu 2) |
| Ingin mengulang Langkah 4 | berkasnya aman dijalankan ulang (ia menghapus `penjualan_bersih` dan view lebih dulu) |

Cara mengulang bersih dari Minggu 2: jalankan lagi Langkah 1, 2, dan 3 Minggu 2 (Langkah 1 menghapus dan membuat ulang ketiga database), lalu Langkah 4–5 minggu ini.

## Yang dikumpulkan ke LMS

1. **Screenshot:** hasil verifikasi yang menunjukkan `penjualan_bersih` = 560, pembagian kasir/Excel = 389/171, dan omzet = 20.784.000.
2. **Jawaban:** sebutkan **satu** masalah pada data Excel Cabang Barat dan bagaimana pembersihan menanganinya (1–3 kalimat).
3. **Opsional:** satu hal yang masih membingungkanmu.

Minggu depan: Sesi 2, skema bintang. Angka 560 dan 20.784.000 harus tetap sama.
