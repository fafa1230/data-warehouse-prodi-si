"""
konfigurasi.py — satu-satunya berkas yang perlu kamu ubah.

Sesuaikan DB_USER dan DB_PASS dengan MySQL/MariaDB di laptopmu,
lalu semua skrip Python di Sesi 4, 5, 7, dan 8 langsung jalan.
"""

import os
from pathlib import Path

# Ubah empat baris ini sesuai MySQL di laptopmu.
# (Kalau mau, nilainya juga bisa diganti lewat environment variable
#  DW_USER / DW_PASS / DW_HOST / DW_PORT tanpa mengubah berkas ini.)
DB_USER = os.environ.get("DW_USER", "root")
DB_PASS = os.environ.get("DW_PASS", "")        # contoh: "rahasia123"
DB_HOST = os.environ.get("DW_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DW_PORT", 3306))


def url(nama_database: str) -> str:
    """Membuat alamat koneksi SQLAlchemy untuk satu database."""
    sandi = f":{DB_PASS}" if DB_PASS else ""
    return f"mysql+pymysql://{DB_USER}{sandi}@{DB_HOST}:{DB_PORT}/{nama_database}"


URL_SUMBER  = url("sumber_kasir")
URL_STAGING = url("staging_toko")
URL_DW      = url("dw_toko")

# Folder-folder penting, dihitung otomatis dari letak berkas ini.
AKAR    = Path(__file__).resolve().parent
DATA    = AKAR / "data"
KELUARAN = AKAR / "keluaran"
KELUARAN.mkdir(exist_ok=True)
