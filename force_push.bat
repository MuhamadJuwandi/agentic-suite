@echo off
echo Memaksa Upload (Force Push)...

git add .
git commit -m "Resolve merge conflict by forcing local version"
git push -u origin main --force

echo.
echo Selesai! Seharusnya sekarang sudah berhasil.
echo Cek repository anda: https://github.com/MuhamadJuwandi/agentic-suite
pause
