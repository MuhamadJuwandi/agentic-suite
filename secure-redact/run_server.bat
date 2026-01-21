@echo off
echo Menyalakan Server API...
echo Buka http://localhost:8000/docs di browser anda setelah server menyala.
uvicorn api.index:app --reload
pause
