@echo off
cd /d "C:\Project\Test"
call .venv\Scripts\activate
echo [1/2] 수집 및 AI 요약 동작 시작...
python main.py
echo [2/2] 로컬 React 개발 서버 기동...
npm.cmd run dev
pause
