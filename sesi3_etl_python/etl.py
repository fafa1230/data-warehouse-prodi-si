"""
SESI 3 — ETL LENGKAP DENGAN PYTHON
Materi: Minggu 9-12 (extract, transform, load)

Satu berkas, tiga bagian, dijalankan berurutan:

  BAGIAN 1  EXTRACT    tarik apa adanya dari MySQL dan dari CSV
  BAGIAN 2  TRANSFORM  bersihkan, seragamkan, catat yang dibuang
  BAGIAN 3  LOAD       muat dimensi dulu, baru fakta, terakhir indeks

Hasil akhirnya HARUS sama persis dengan Sesi 1 yang memakai SQL:
560 baris dan omzet 20.784.000. Dua jalan berbeda, satu angka yang sama.
Itulah bukti bahwa ETL bukan sihir, hanya cara lain menempuh jalan yang sama.

Jalankan dari folder praktikum-dw-inti:
    python sesi3_etl_python/etl.py
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

sys.path.append(str(Path(__file__).resolve().parent.parent))
import konfigurasi as cfg

KUNCI_TIDAK_DIKETAHUI = -1
catatan = []          # log: (langkah, masuk, dibuang, keluar)


def lapor(langkah, masuk, keluar):
    catatan.append((langkah, masuk, masuk - keluar, keluar))


# =====================================================================
# BAGIAN 1 — EXTRACT
# Tugasnya HANYA menarik. Tidak ada pembersihan sama sekali di sini.
# Makin cepat kita melepaskan sistem sumber, makin kecil gangguannya
# ke aplikasi kasir yang sedang melayani pembeli.
# =====================================================================

def extract_kasir(mesin_sumber) -> pd.DataFrame:
    """Sumber 1: database aplikasi kasir (Cabang Pusat dan Timur)."""
    sql = """
        SELECT n.id_nota, n.tanggal, c.nama_cabang, c.kota AS kota_cabang,
               p.nama_produk, p.kategori, i.jumlah, p.harga AS harga_satuan,
               n.id_pelanggan
        FROM nota_item i
        JOIN nota   n ON i.id_nota   = n.id_nota
        JOIN produk p ON i.id_produk = p.id_produk
        JOIN cabang c ON n.id_cabang = c.id_cabang
    """
    return pd.read_sql(sql, mesin_sumber)


def extract_barat() -> pd.DataFrame:
    """Sumber 2: ekspor Excel Cabang Barat.

    dtype=str itu disengaja, sikapnya sama dengan kolom VARCHAR di
    staging Sesi 1: jangan memaksakan tipe data sebelum tahu isinya bersih.
    """
    return pd.read_csv(cfg.DATA / "penjualan_barat.csv", dtype=str)


def extract_produk(mesin_sumber) -> pd.DataFrame:
    """Tabel rujukan produk, dipakai untuk menyeragamkan nama."""
    return pd.read_sql(
        "SELECT id_produk, nama_produk, kategori, harga FROM produk", mesin_sumber)


# =====================================================================
# BAGIAN 2 — TRANSFORM
# Di sinilah data diperbaiki, dan di sinilah sebagian besar waktu habis.
# Setiap langkah mencatat berapa baris masuk dan berapa yang dibuang.
# =====================================================================

def transform_kasir(df: pd.DataFrame) -> pd.DataFrame:
    """Data kasir sudah rapi. Hanya perlu disamakan bentuk kolomnya."""
    masuk = len(df)
    hasil = pd.DataFrame({
        "no_nota":      "NOTA-" + df["id_nota"].astype(str),
        "tanggal":      pd.to_datetime(df["tanggal"]),
        "nama_cabang":  df["nama_cabang"],
        "kota_cabang":  df["kota_cabang"],
        "nama_produk":  df["nama_produk"],
        "kategori":     df["kategori"],
        "jumlah":       df["jumlah"].astype(int),
        "harga_satuan": df["harga_satuan"].astype(int),
        "id_pelanggan": df["id_pelanggan"],
        "sumber":       "kasir",
    })
    lapor("Kasir: menyamakan bentuk kolom", masuk, len(hasil))
    return hasil


def transform_barat(df: pd.DataFrame, produk: pd.DataFrame) -> pd.DataFrame:
    """Data Excel Cabang Barat: inilah yang benar-benar perlu dibersihkan."""
    masuk = len(df)
    df = df.copy()

    # --- 1. buang baris yang jumlahnya kosong -------------------------
    df["jumlah"] = df["jumlah"].fillna("").astype(str).str.strip()
    df = df[df["jumlah"] != ""]
    lapor("Excel: membuang baris tanpa jumlah", masuk, len(df))

    # --- 2. buang baris duplikat --------------------------------------
    sebelum = len(df)
    df = df.drop_duplicates()
    lapor("Excel: membuang baris duplikat", sebelum, len(df))

    # --- 3. seragamkan nama produk lewat tabel rujukan -----------------
    # BUKAN dengan .str.title(). Mencocokkan ke tabel produk resmi selalu
    # aman, sedangkan mengubah huruf besar-kecil bisa meleset untuk nama
    # yang lebih rumit.
    sebelum = len(df)
    df["kunci"] = df["nama_produk"].str.strip().str.upper()
    produk = produk.copy()
    produk["kunci"] = produk["nama_produk"].str.upper()
    df = df.merge(produk[["kunci", "nama_produk", "kategori"]],
                  on="kunci", how="left", suffixes=("_asli", ""))
    tidak_cocok = int(df["nama_produk"].isna().sum())
    if tidak_cocok:
        print(f"PERINGATAN: {tidak_cocok} baris tidak cocok ke tabel produk.")
    df = df[df["nama_produk"].notna()]
    lapor("Excel: mencocokkan nama produk", sebelum, len(df))

    # --- 4. ubah tipe data --------------------------------------------
    return pd.DataFrame({
        "no_nota":      df["no_nota"].str.strip(),
        "tanggal":      pd.to_datetime(df["tanggal"], format="%d/%m/%Y"),
        "nama_cabang":  "Cabang Barat",
        "kota_cabang":  "Ungaran",
        "nama_produk":  df["nama_produk"],
        "kategori":     df["kategori"],
        "jumlah":       df["jumlah"].astype(int),
        "harga_satuan": df["harga_satuan"].astype(int),
        "id_pelanggan": pd.to_numeric(df["id_pelanggan"], errors="coerce"),
        "sumber":       "excel",
    })


# =====================================================================
# BAGIAN 3 — LOAD
# Aturan yang tidak bisa ditawar:
#   SEMUA DIMENSI DIMUAT SAMPAI SELESAI DULU, BARU TABEL FAKTA.
# Kunci dimensi baru ada setelah baris dimensinya terbentuk, sedangkan
# tabel fakta membutuhkan kunci itu.
# =====================================================================

NAMA_HARI = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis",
             4: "Jumat", 5: "Sabtu", 6: "Minggu"}
NAMA_BULAN = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
              5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
              9: "September", 10: "Oktober", 11: "November", 12: "Desember"}


def muat_dimensi(mesin_dw, mesin_sumber, bersih: pd.DataFrame) -> dict:
    # dimensi tanggal: satu tahun penuh, bukan hanya tanggal yang ada
    # transaksinya, supaya hari tanpa penjualan tetap bisa dilaporkan
    t = pd.DataFrame({"tanggal": pd.date_range("2026-01-01", "2026-12-31", freq="D")})
    t["tanggal_key"] = t["tanggal"].dt.strftime("%Y%m%d").astype(int)
    t["tahun"] = t["tanggal"].dt.year
    t["bulan"] = t["tanggal"].dt.month
    t["nama_bulan"] = t["bulan"].map(NAMA_BULAN)
    t["nama_hari"] = t["tanggal"].dt.dayofweek.map(NAMA_HARI)
    t["kuartal"] = t["tanggal"].dt.quarter
    t["akhir_pekan"] = t["tanggal"].dt.dayofweek.ge(5).map({True: "Ya", False: "Tidak"})
    dim_tanggal = t[["tanggal_key", "tanggal", "tahun", "bulan",
                     "nama_bulan", "nama_hari", "kuartal", "akhir_pekan"]]

    dim_produk = (bersih[["nama_produk", "kategori", "harga_satuan"]]
                  .drop_duplicates("nama_produk").sort_values("nama_produk")
                  .reset_index(drop=True)
                  .rename(columns={"harga_satuan": "harga_berlaku"}))
    dim_produk.insert(0, "produk_key", range(1, len(dim_produk) + 1))
    dim_produk = pd.concat([pd.DataFrame([{
        "produk_key": KUNCI_TIDAK_DIKETAHUI, "nama_produk": "Tidak Diketahui",
        "kategori": "Tidak Diketahui", "harga_berlaku": 0}]),
        dim_produk], ignore_index=True)

    dim_cabang = (bersih[["nama_cabang", "kota_cabang"]]
                  .drop_duplicates("nama_cabang").sort_values("nama_cabang")
                  .reset_index(drop=True))
    dim_cabang.insert(0, "cabang_key", range(1, len(dim_cabang) + 1))
    dim_cabang = pd.concat([pd.DataFrame([{
        "cabang_key": KUNCI_TIDAK_DIKETAHUI,
        "nama_cabang": "Tidak Diketahui", "kota_cabang": "-"}]),
        dim_cabang], ignore_index=True)

    pelanggan = pd.read_sql("SELECT id_pelanggan, nama_pelanggan, kota, "
                            "tanggal_daftar FROM pelanggan", mesin_sumber)
    pelanggan.insert(0, "pelanggan_key", range(1, len(pelanggan) + 1))
    dim_pelanggan = pd.concat([pd.DataFrame([{
        "pelanggan_key": KUNCI_TIDAK_DIKETAHUI,
        "id_pelanggan": KUNCI_TIDAK_DIKETAHUI,
        "nama_pelanggan": "Tanpa Identitas", "kota": "-",
        "tanggal_daftar": None}]), pelanggan], ignore_index=True)

    dimensi = {"dim_tanggal_py": dim_tanggal, "dim_produk_py": dim_produk,
               "dim_cabang_py": dim_cabang, "dim_pelanggan_py": dim_pelanggan}
    for nama, df in dimensi.items():
        df.to_sql(nama, mesin_dw, if_exists="replace", index=False)
    return dimensi


def muat_fakta(mesin_dw, bersih: pd.DataFrame, dimensi: dict) -> pd.DataFrame:
    """Menukar setiap nama menjadi kunci angka, lalu menulis tabel fakta."""
    f = bersih.copy()
    f["tanggal"] = pd.to_datetime(f["tanggal"])
    f["id_pelanggan"] = f["id_pelanggan"].fillna(KUNCI_TIDAK_DIKETAHUI).astype(int)

    # how="left" supaya baris yang gagal dicocokkan TIDAK hilang diam-diam
    f = (f.merge(dimensi["dim_tanggal_py"][["tanggal", "tanggal_key"]],
                 on="tanggal", how="left")
          .merge(dimensi["dim_produk_py"][["nama_produk", "produk_key"]],
                 on="nama_produk", how="left")
          .merge(dimensi["dim_cabang_py"][["nama_cabang", "cabang_key"]],
                 on="nama_cabang", how="left")
          .merge(dimensi["dim_pelanggan_py"][["id_pelanggan", "pelanggan_key"]],
                 on="id_pelanggan", how="left"))
    for kolom in ["tanggal_key", "produk_key", "cabang_key", "pelanggan_key"]:
        f[kolom] = f[kolom].fillna(KUNCI_TIDAK_DIKETAHUI).astype(int)

    fakta = f[["tanggal_key", "produk_key", "cabang_key", "pelanggan_key",
               "no_nota", "jumlah", "harga_satuan", "total"]]
    fakta.to_sql("fact_penjualan_py", mesin_dw, if_exists="replace", index=False)
    return fakta


def buat_indeks(mesin_dw):
    """Langkah terakhir yang paling sering dilupakan.

    Tabel hasil to_sql() sama sekali tidak punya indeks, sehingga join di
    Sesi 4 bisa berjalan berpuluh kali lebih lambat. Indeks SELALU dibuat
    SESUDAH data dimuat, bukan sebelumnya.
    """
    perintah = [
        "ALTER TABLE dim_tanggal_py   ADD PRIMARY KEY (tanggal_key)",
        "ALTER TABLE dim_produk_py    ADD PRIMARY KEY (produk_key)",
        "ALTER TABLE dim_cabang_py    ADD PRIMARY KEY (cabang_key)",
        "ALTER TABLE dim_pelanggan_py ADD PRIMARY KEY (pelanggan_key)",
        "ALTER TABLE fact_penjualan_py "
        "  ADD INDEX i_tanggal (tanggal_key), ADD INDEX i_produk (produk_key), "
        "  ADD INDEX i_cabang (cabang_key),   ADD INDEX i_pelanggan (pelanggan_key)",
    ]
    with mesin_dw.begin() as c:
        for p in perintah:
            c.execute(text(p))


# =====================================================================
# Jalannya proses
# =====================================================================

if __name__ == "__main__":
    mesin_sumber = create_engine(cfg.URL_SUMBER)
    mesin_dw     = create_engine(cfg.URL_DW)

    print("=" * 64)
    print("  BAGIAN 1 - EXTRACT")
    print("=" * 64)
    kasir  = extract_kasir(mesin_sumber)
    barat  = extract_barat()
    produk = extract_produk(mesin_sumber)
    print(f"Dari database kasir : {len(kasir):>4} baris")
    print(f"Dari file Excel     : {len(barat):>4} baris")
    print(f"Tabel rujukan produk: {len(produk):>4} baris")
    print()
    print("Lima baris pertama data Excel, perhatikan betapa berantakannya:")
    print(barat.head().to_string(index=False))

    print()
    print("=" * 64)
    print("  BAGIAN 2 - TRANSFORM")
    print("=" * 64)
    bersih = pd.concat([transform_kasir(kasir), transform_barat(barat, produk)],
                       ignore_index=True)
    bersih["total"] = bersih["jumlah"] * bersih["harga_satuan"]
    bersih = bersih[["no_nota", "tanggal", "nama_cabang", "kota_cabang",
                     "nama_produk", "kategori", "jumlah", "harga_satuan",
                     "total", "id_pelanggan", "sumber"]]
    bersih.to_csv(cfg.KELUARAN / "penjualan_bersih.csv", index=False)

    print(f"{'Langkah':<38}{'masuk':>8}{'dibuang':>9}{'keluar':>8}")
    print("-" * 63)
    for langkah, masuk, dibuang, keluar in catatan:
        print(f"{langkah:<38}{masuk:>8}{dibuang:>9}{keluar:>8}")
    print("-" * 63)
    print(f"{'HASIL AKHIR':<38}{'':>8}{'':>9}{len(bersih):>8}")
    print()
    print(f"Jumlah produk berbeda : {bersih['nama_produk'].nunique()}")
    print(f"Tanggal gagal dibaca  : {bersih['tanggal'].isna().sum()}")

    print()
    print("=" * 64)
    print("  BAGIAN 3 - LOAD")
    print("=" * 64)
    bersih.to_sql("penjualan_bersih_py", mesin_dw, if_exists="replace", index=False)
    dimensi = muat_dimensi(mesin_dw, mesin_sumber, bersih)   # DIMENSI DULU
    fakta   = muat_fakta(mesin_dw, bersih, dimensi)          # BARU FAKTA
    buat_indeks(mesin_dw)                                    # INDEKS PALING AKHIR

    for nama, df in dimensi.items():
        print(f"{nama:<20}: {len(df):>4} baris")
    print(f"{'fact_penjualan_py':<20}: {len(fakta):>4} baris")

    gagal = {k: int((fakta[k] == KUNCI_TIDAK_DIKETAHUI).sum())
             for k in ["tanggal_key", "produk_key", "cabang_key"]}
    print()
    print(f"Omzet di tabel fakta : {fakta['total'].sum():,}".replace(",", "."))
    print(f"Gagal lookup         : {gagal}  (semuanya harus 0)")
    print(f"Tanpa identitas      : "
          f"{(fakta['pelanggan_key'] == KUNCI_TIDAK_DIKETAHUI).sum()} baris")
    print()
    print("Bandingkan dengan hasil Sesi 1 yang memakai SQL. Harus sama persis.")
