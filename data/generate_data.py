"""
generate_data.py — membuat data sumber untuk praktikum.

Dijalankan SEKALI sebelum Sesi 1.
Ukurannya sengaja kecil (ratusan baris, bukan ribuan) supaya ringan di
laptop berspesifikasi minimal: seluruh praktikum berjalan di bawah
sepuluh megabyte dan tiap query selesai dalam hitungan detik.

Hasilnya:
  data/seed_sumber.sql      -> INSERT untuk database sumber_kasir (Cabang Pusat & Timur)
  data/penjualan_barat.csv  -> ekspor Excel Cabang Barat (sengaja berantakan)

Angka acak memakai seed tetap, jadi hasilnya selalu sama di semua laptop
dan semua angka verifikasi di modul berlaku untuk setiap orang.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)
HERE = Path(__file__).resolve().parent

MULAI, SELESAI = date(2026, 1, 1), date(2026, 3, 31)   # satu kuartal
JUMLAH_PELANGGAN = 40

CABANG = [
    (1, "Cabang Pusat", "Semarang"),
    (2, "Cabang Timur", "Semarang"),
    (3, "Cabang Barat", "Ungaran"),
]

PRODUK = [
    (1, "Roti Coklat", "Roti", 8000),
    (2, "Roti Keju", "Roti", 9000),
    (3, "Roti Sobek", "Roti", 15000),
    (4, "Donat Gula", "Donat", 5000),
    (5, "Donat Coklat", "Donat", 6000),
    (6, "Bolu Pandan", "Kue", 22000),
    (7, "Brownies", "Kue", 25000),
    (8, "Lapis Legit", "Kue", 45000),
]

DEPAN = ["Andi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hadi",
         "Indah", "Joko", "Kartika", "Lukman", "Maya", "Nanda", "Putri", "Sari"]
BELAKANG = ["Pratama", "Santoso", "Wijaya", "Lestari", "Nugroho", "Hidayat"]
KOTA_PELANGGAN = ["Semarang", "Ungaran", "Salatiga", "Demak"]

# Produk yang sering dibeli bersama, supaya polanya bisa terlihat di Sesi 4
PASANGAN = [(1, 4), (3, 5), (6, 7)]


def buat_pelanggan(n=JUMLAH_PELANGGAN):
    baris = []
    for i in range(1, n + 1):
        nama = f"{random.choice(DEPAN)} {random.choice(BELAKANG)}"
        kota = random.choice(KOTA_PELANGGAN)
        daftar = date(2025, 1, 1) + timedelta(days=random.randint(0, 400))
        baris.append((i, nama, kota, daftar.isoformat()))
    return baris


def buat_nota():
    """Kembalikan daftar (id_nota, tanggal, id_cabang, id_pelanggan, items)."""
    notas, nomor, hari = [], 1, MULAI
    while hari <= SELESAI:
        # akhir pekan sedikit lebih ramai
        jumlah_nota = random.randint(4, 6) if hari.weekday() >= 5 else random.randint(2, 4)
        for _ in range(jumlah_nota):
            id_cabang = random.choices([1, 2, 3], weights=[40, 30, 30])[0]
            id_pelanggan = random.randint(1, JUMLAH_PELANGGAN) if random.random() < 0.7 else None

            items = {}
            n_item = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
            if n_item >= 2 and random.random() < 0.5:
                a, b = random.choice(PASANGAN)
                items[a] = random.randint(1, 3)
                items[b] = random.randint(1, 3)
            while len(items) < n_item:
                p = random.randint(1, len(PRODUK))
                if p not in items:
                    items[p] = random.randint(1, 4)

            notas.append((nomor, hari, id_cabang, id_pelanggan, items))
            nomor += 1
        hari += timedelta(days=1)
    return notas


def tulis_seed_sql(notas, pelanggan):
    """INSERT untuk nota cabang 1 dan 2, yang ada di database kasir."""
    bagian = ["INSERT INTO pelanggan VALUES"]
    bagian.append(",\n".join(f"  ({i},'{n}','{k}','{d}')" for i, n, k, d in pelanggan) + ";\n")

    nota_sql, item_sql = [], []
    for nomor, hari, id_cabang, id_pelanggan, items in notas:
        if id_cabang == 3:
            continue                        # Cabang Barat tidak ada di kasir
        pel = str(id_pelanggan) if id_pelanggan else "NULL"
        nota_sql.append(f"  ({nomor},'{hari.isoformat()}',{id_cabang},{pel})")
        for id_produk, jumlah in items.items():
            item_sql.append(f"  ({nomor},{id_produk},{jumlah})")

    bagian.append("INSERT INTO nota VALUES")
    bagian.append(",\n".join(nota_sql) + ";\n")
    bagian.append("INSERT INTO nota_item (id_nota,id_produk,jumlah) VALUES")
    bagian.append(",\n".join(item_sql) + ";\n")

    (HERE / "seed_sumber.sql").write_text("\n".join(bagian), encoding="utf-8")
    return len(nota_sql), len(item_sql)


def kotori_nama(nama):
    """Meniru pengetikan manual di Excel: huruf besar-kecil tidak konsisten."""
    gaya = random.random()
    if gaya < 0.25:
        return nama.upper()
    if gaya < 0.50:
        return nama.lower()
    if gaya < 0.65:
        return "  " + nama + " "
    return nama


def tulis_csv_barat(notas):
    """Ekspor Cabang Barat: tanggal dd/mm/yyyy, nama produk tidak seragam."""
    harga = {p[0]: p[3] for p in PRODUK}
    nama_produk = {p[0]: p[1] for p in PRODUK}

    baris = []
    for nomor, hari, id_cabang, id_pelanggan, items in notas:
        if id_cabang != 3:
            continue
        for id_produk, jumlah in items.items():
            baris.append([f"NOTA-{nomor}", hari.strftime("%d/%m/%Y"),
                          kotori_nama(nama_produk[id_produk]),
                          str(jumlah), str(harga[id_produk]),
                          str(id_pelanggan) if id_pelanggan else ""])

    bersih = len(baris)
    # 12 baris duplikat: kesalahan salin-tempel yang lazim terjadi
    for b in random.sample(baris, 12):
        baris.append(list(b))
    # 5 baris dengan jumlah kosong, harus dibuang saat transform
    for b in random.sample(baris, 5):
        rusak = list(b)
        rusak[3] = ""
        baris.append(rusak)
    random.shuffle(baris)

    # lineterminator="\n" penting: kalau memakai \r\n bawaan, MySQL ikut
    # membaca karakter \r ke kolom terakhir dan LOAD DATA gagal.
    with open(HERE / "penjualan_barat.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["no_nota", "tanggal", "nama_produk", "jumlah",
                    "harga_satuan", "id_pelanggan"])
        w.writerows(baris)
    return bersih, len(baris)


if __name__ == "__main__":
    pelanggan = buat_pelanggan()
    notas = buat_nota()
    n_nota, n_item = tulis_seed_sql(notas, pelanggan)
    bersih, total_csv = tulis_csv_barat(notas)

    print("=== Data sumber berhasil dibuat ===")
    print(f"Periode                : {MULAI} sampai {SELESAI}")
    print(f"seed_sumber.sql        : {n_nota} nota, {n_item} baris item (Cabang Pusat & Timur)")
    print(f"penjualan_barat.csv    : {total_csv} baris ({bersih} asli + 12 duplikat + 5 kosong)")
    print(f"pelanggan              : {len(pelanggan)} orang")
    print(f"produk                 : {len(PRODUK)} jenis")
    print()
    print(f"Perkiraan isi gudang   : {n_item + bersih} baris")
