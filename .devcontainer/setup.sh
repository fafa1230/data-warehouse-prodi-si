#!/usr/bin/env bash
# Dijalankan sekali saat Codespace pertama kali dibuat.
set -e

echo "==> Memasang pustaka Python"
pip install --no-cache-dir --quiet -r requirements.txt

echo "==> Memasang klien MariaDB"
sudo apt-get update -qq
sudo apt-get install -y -qq mariadb-client >/dev/null

echo "==> Menyimpan pengaturan koneksi"
cat > "$HOME/.my.cnf" <<'CNF'
[client]
host=db
user=root
password=praktikum
local-infile=1
CNF
chmod 600 "$HOME/.my.cnf"

echo "==> Menunggu server MariaDB siap"
for _ in $(seq 1 60); do
    if mariadb -e "SELECT 1" >/dev/null 2>&1; then
        break
    fi
    sleep 2
done

echo "==> Membuat data sumber"
python data/generate_data.py

echo
echo "Lingkungan siap."
echo "Periksa dulu dengan:  python cek_pemasangan.py"
echo "Di sini, tiap perintah 'mysql -u root -p' di modul cukup ditulis 'mariadb'."
