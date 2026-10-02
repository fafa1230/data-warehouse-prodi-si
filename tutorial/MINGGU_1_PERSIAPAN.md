# Tutorial Minggu 1 — Persiapan

**Tujuan minggu ini:** laptopmu (atau Codespaces) siap menjalankan praktikum.
**Target:** `python cek_pemasangan.py` menunjukkan semua pemeriksaan lolos.
**Waktu:** sekitar 30–60 menit, sebagian besar untuk mengunduh dan memasang.

Pilih **satu** jalur. Kalau ragu, pilih Jalur A.

| Jalur | Cocok untuk | Perlu memasang? |
| --- | --- | --- |
| A. Codespaces | RAM di bawah 4 GB, laptop lama, atau malas memasang | Tidak |
| B. Komputer sendiri | Laptop dengan RAM 4 GB ke atas | Ya: MariaDB dan Python |

---

## Jalur A — Codespaces (tanpa memasang apa pun)

1. Punya akun GitHub (gratis). Masuk ke https://github.com.
2. Buka https://github.com/fafa1230/data-warehouse-prodi-si
3. Klik tombol hijau **Code**, pilih tab **Codespaces**, lalu **Create codespace on main**.
4. Tunggu beberapa menit sampai tampil editor di browser. MariaDB, Python, pustaka, dan data sumber disiapkan otomatis.
5. Buka terminal di bagian bawah editor, lalu lanjut ke **Langkah pemeriksaan** di bawah.

Catatan Codespaces:
- Perintah `mysql -u root -p` di modul cukup ditulis `mariadb`.
- Perubahanmu hanya tersimpan di salinan pribadimu, tidak mengubah repo dosen.
- Hentikan Codespace kalau sudah selesai (Settings → Codespaces) agar jatah gratis tidak habis.

---

## Jalur B — Komputer sendiri

### B1. Ambil repo (pilih salah satu)

**Tanpa git:** buka halaman repo, klik **Code → Download ZIP**, lalu ekstrak. Ini paling sederhana.

**Dengan git:**

```bash
git clone https://github.com/fafa1230/data-warehouse-prodi-si.git
cd data-warehouse-prodi-si
```

### B2. Pasang MariaDB (atau MySQL 8)

- Unduh dari situs resmi MariaDB (https://mariadb.org/download) dan pasang dengan pilihan bawaan.
- Saat pemasangan, kamu diminta membuat **sandi untuk pengguna `root`**. Catat sandinya, nanti dipakai.
- Pasang **MariaDB saja, jangan XAMPP**. XAMPP membawa Apache dan PHP yang tidak dipakai di mata kuliah ini.
- Kalau RAM-mu 4 GB, jalankan SQL lewat perintah `mysql`, bukan Workbench atau DBeaver, karena keduanya memakan 300–500 MB memori.

### B3. Pasang Python 3.9 atau lebih baru

Unduh dari https://www.python.org/downloads. Di Windows, **centang "Add Python to PATH"** pada layar pertama pemasang. Periksa:

```bash
python --version
```

(Di macOS atau Linux, kalau tidak dikenali, coba `python3 --version`, dan pakai `python3` sebagai ganti `python` di seluruh tutorial.)

### B4. Pasang pustaka Python

Dari folder utama repo:

```bash
pip install -r requirements.txt
```

Isinya hanya tiga pustaka: `pandas`, `SQLAlchemy`, `PyMySQL`.

### B5. Beri tahu skrip cara masuk ke MySQL-mu

Cara paling aman, lewat variabel lingkungan. Sandimu tidak tersimpan di berkas mana pun.

macOS/Linux:

```bash
export DW_USER=root
export DW_PASS=sandimu
```

Windows PowerShell:

```powershell
$env:DW_USER="root"
$env:DW_PASS="sandimu"
```

Ganti `sandimu` dengan sandi `root` yang kamu buat tadi. Variabel ini hanya berlaku di jendela terminal itu, jadi ulangi kalau kamu membuka terminal baru.

> **Jangan menulis sandi langsung di `konfigurasi.py` lalu mengunggahnya ke GitHub.**

### B6. Buat data sumber

```bash
python data/generate_data.py
```

---

## Langkah pemeriksaan (semua jalur)

Pastikan terminal berada di **folder utama repo** (folder yang berisi `README.md`, `konfigurasi.py`, dan folder `data/`). Folder ini bernama sama dengan nama repo atau hasil ekstrak ZIP-nya. Jalankan:

```bash
python cek_pemasangan.py
```

Skrip memeriksa RAM dan sisa disk, versi Python, tiga pustaka, dua berkas data, dan koneksi ke MySQL. Hasil yang kamu inginkan: semua pemeriksaan lolos.

Kalau ada yang gagal, skrip menyebutkan apa yang kurang dan cara memperbaikinya. Perbaiki, lalu jalankan lagi sampai bersih.

## Kalau tersendat

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| `python` tidak dikenali | Python belum masuk PATH | Pasang ulang dan centang "Add Python to PATH", atau coba `python3` |
| `pip` tidak dikenali | Sama seperti di atas | Coba `python -m pip install -r requirements.txt` |
| `Access denied for user` | Sandi salah atau belum diatur | Cek `DW_PASS`; atur ulang variabel di terminal yang sedang dipakai |
| Koneksi MySQL gagal | Server belum berjalan | Nyalakan layanan MariaDB (Services di Windows, `brew services start mariadb` di macOS) |
| `File ... not found` | Folder kerja salah | `cd` ke folder utama repo, bukan ke folder sesi |
| Laptop sangat lambat | RAM terlalu kecil | Tutup aplikasi lain, atau pakai Jalur A |

## Yang dikumpulkan ke LMS

1. **Screenshot** hasil `python cek_pemasangan.py` yang menunjukkan semua pemeriksaan lolos. Pastikan **sandimu tidak terlihat** di layar.
2. **Jawaban satu pertanyaan:** mengapa semua perintah dijalankan dari folder utama repo, bukan dari dalam folder sesi?
3. **Opsional:** satu hal yang masih membingungkanmu.

Minggu depan: Sesi 1, arsitektur tiga lapis dan staging.
