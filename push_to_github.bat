@echo off
echo Mengupload ke GitHub...

git init
git add .
git commit -m "Initial commit: Added SecureRedact API to Agentic Suite"
git branch -M main
git remote add origin https://github.com/MuhamadJuwandi/agentic-suite.git
git push -u origin main

echo.
echo Selesai! Cek repository anda di: https://github.com/MuhamadJuwandi/agentic-suite
pause
