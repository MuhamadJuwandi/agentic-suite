@echo off
echo Memperbaiki masalah upload GitHub...

echo 1. Mengambil file dari GitHub (README/License)...
git pull origin main --allow-unrelated-histories

echo.
echo 2. Mengupload ulang kode kita...
git push -u origin main

echo.
echo Selesai! Cek repository anda: https://github.com/MuhamadJuwandi/agentic-suite
pause
