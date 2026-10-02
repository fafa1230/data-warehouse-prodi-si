"""
cek_pemasangan.py — memeriksa apakah laptopmu sudah siap praktikum.

Jalankan ini SEBELUM Sesi 1. Skrip akan memeriksa satu per satu dan
memberi tahu persis apa yang kurang serta cara memperbaikinya.

    python cek_pemasangan.py
"""

import os
import shutil
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent
sys.path.append(str(AKAR))

CENTANG, SILANG, SERU = "[ OK ]", "[GAGAL]", "[ ! ]"
masalah = []
MIN_DISK_GB = 2        # ruang kosong minimal: MySQL + Python + pustakanya


def lapor(status, judul, pesan=""):
    print(f"{status:<8}{judul}")
    if pesan:
        print(f"        {pesan}")


def _ram_gb():
    """Kapasitas RAM dalam GB. None kalau tidak bisa dibaca."""
    try:
        if hasattr(os, "sysconf") and "SC_PHYS_PAGES" in os.sysconf_names:
            return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3
    except (ValueError, OSError):
        pass
    try:                                        # Windows
        import ctypes

        class _Mem(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

        info = _Mem()
        info.dwLength = ctypes.sizeof(_Mem)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(info))
        return info.ullTotalPhys / 1024 ** 3
    except Exception:
        pass
    try:                                        # macOS lama
        import subprocess
        keluaran = subprocess.run(["sysctl", "-n", "hw.memsize"],
                                  capture_output=True, text=True, timeout=5)
        return int(keluaran.stdout.strip()) / 1024 ** 3
    except Exception:
        return None


def cek_perangkat():
    """Memeriksa RAM dan sisa disk, lalu menyarankan jalur yang paling pas."""
    if sys.maxsize <= 2 ** 32:
        lapor(SILANG, "Sistem 32-bit")
        masalah.append("MySQL 8 dan MariaDB terbaru butuh sistem operasi 64-bit. "
                       "Pakai komputer lain atau GitHub Codespaces.")

    ram = _ram_gb()
    if ram is None:
        lapor(SERU, "Kapasitas RAM tidak terbaca", "lewati pemeriksaan ini")
    elif ram >= 7.5:
        lapor(CENTANG, f"RAM {ram:.0f} GB", "cukup untuk semua perkakas")
    elif ram >= 3.5:
        lapor(SERU, f"RAM {ram:.0f} GB",
              "cukup, tapi jalankan SQL lewat perintah mysql, "
              "jangan lewat MySQL Workbench atau DBeaver")
    else:
        lapor(SILANG, f"RAM {ram:.1f} GB terlalu kecil")
        masalah.append("RAM di bawah 4 GB. Pakai komputer laboratorium, "
                       "atau jalankan praktikum di GitHub Codespaces.")

    try:
        sisa = shutil.disk_usage(AKAR).free / 1024 ** 3
        if sisa >= MIN_DISK_GB:
            lapor(CENTANG, f"Sisa disk {sisa:.1f} GB")
        else:
            lapor(SILANG, f"Sisa disk {sisa:.1f} GB kurang")
            masalah.append(f"Sediakan minimal {MIN_DISK_GB} GB ruang kosong "
                           "untuk MySQL, Python, dan pustakanya.")
    except Exception:
        lapor(SERU, "Sisa disk tidak terbaca", "lewati pemeriksaan ini")


def cek_python():
    v = sys.version_info
    versi = f"{v.major}.{v.minor}.{v.micro}"
    if v >= (3, 9):
        lapor(CENTANG, f"Python {versi}")
    else:
        lapor(SILANG, f"Python {versi} terlalu lama")
        masalah.append("Pasang Python 3.9 atau lebih baru dari python.org")


def cek_pustaka():
    wajib = {
        "pandas": "pandas",
        "sqlalchemy": "SQLAlchemy",
        "pymysql": "PyMySQL",
    }
    kurang = []
    for modul, nama_pip in wajib.items():
        try:
            __import__(modul)
            lapor(CENTANG, f"Pustaka {nama_pip}")
        except ImportError:
            lapor(SILANG, f"Pustaka {nama_pip} belum ada")
            kurang.append(nama_pip)
    if kurang:
        masalah.append("Jalankan: pip install -r requirements.txt")


def cek_berkas_data():
    perlu = ["seed_sumber.sql", "penjualan_barat.csv"]
    hilang = [b for b in perlu if not (AKAR / "data" / b).exists()]
    if hilang:
        lapor(SERU, "Berkas data belum dibuat", f"belum ada: {', '.join(hilang)}")
        masalah.append("Jalankan: python data/generate_data.py")
    else:
        lapor(CENTANG, "Berkas data sumber lengkap")


def cek_koneksi():
    try:
        import konfigurasi as cfg
        from sqlalchemy import create_engine, text
    except ImportError:
        lapor(SILANG, "Koneksi MySQL tidak bisa diuji", "pustaka belum lengkap")
        return

    alamat = cfg.url("information_schema")
    try:
        mesin = create_engine(alamat, connect_args={"connect_timeout": 5})
        with mesin.connect() as c:
            versi = c.execute(text("SELECT VERSION()")).scalar()
        lapor(CENTANG, f"Koneksi MySQL berhasil (server {versi})")
    except Exception as e:
        pesan = str(e).split("\n")[0][:110]
        lapor(SILANG, "Koneksi MySQL gagal", pesan)
        if "Access denied" in str(e):
            masalah.append("Kata sandi salah. Perbaiki DB_PASS di konfigurasi.py "
                           "(kalau memakai XAMPP, biasanya kosong)")
        else:
            masalah.append("Server MySQL belum jalan. Buka XAMPP Control Panel "
                           "lalu klik Start pada baris MySQL")
        return

    # Database praktikum sudah dibuat atau belum
    try:
        with create_engine(alamat).connect() as c:
            ada = {r[0] for r in c.execute(text("SHOW DATABASES"))}
        perlu = {"sumber_kasir", "staging_toko", "dw_toko"}
        kurang = perlu - ada
        if kurang:
            lapor(SERU, "Database praktikum belum dibuat",
                  f"belum ada: {', '.join(sorted(kurang))} (normal sebelum Sesi 1)")
        else:
            lapor(CENTANG, "Ketiga database praktikum sudah ada")
    except Exception:
        pass


if __name__ == "__main__":
    print("=" * 66)
    print("  PEMERIKSAAN KESIAPAN PRAKTIKUM DATA WAREHOUSE")
    print("=" * 66)
    print()
    cek_perangkat()
    cek_python()
    cek_pustaka()
    cek_berkas_data()
    cek_koneksi()
    print()
    print("-" * 66)
    if masalah:
        print(f"Ada {len(masalah)} hal yang perlu dibereskan:")
        for i, m in enumerate(masalah, 1):
            print(f"  {i}. {m}")
        print()
        print("Perbaiki lalu jalankan skrip ini lagi.")
        sys.exit(1)
    print("SEMUA SIAP. Silakan mulai Sesi 1.")
