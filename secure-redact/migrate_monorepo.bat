@echo off
echo Membuat Struktur Monorepo 'agentic-suite'...

cd ..
if not exist "agentic-suite" mkdir "agentic-suite"
cd "agentic-suite"
if not exist "secure-redact" mkdir "secure-redact"

echo Memindahkan File Project 1 ke secure-redact...
xcopy /E /Y "..\PROJECT 1\*" "secure-redact\"

echo Membuat README root...
echo # Agentic Suite > README.md
echo A premium collection of serverless AI Agents. >> README.md

echo Selesai! Struktur Monorepo telah dibuat.
echo Silakan buka folder 'API PROJECT\agentic-suite' untuk push ke GitHub.
pause
