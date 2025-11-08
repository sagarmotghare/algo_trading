@echo off
echo === AlgoTrading ===
echo An algorithmic trading system designed to train predictive models and operate on live market data.
echo.

if exist ".venv\" (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Using global environment.
)
echo.

:: Launch Python and capture its PID using PowerShell
powershell -Command "Start-Process python -ArgumentList 'live.py' -PassThru | Select-Object -ExpandProperty Id | Out-File -Encoding ASCII -NoNewline pid.txt"

:: Confirm PID saved
set /p PY_PID=<pid.txt
echo Python PID: %PY_PID%
echo PID saved to pid.txt
echo.

pause