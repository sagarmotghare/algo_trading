@echo off
echo Scheduling AlgoTrading tasks...

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Schedule start.bat at 9:10 AM daily
schtasks /create /tn "AlgoTradingStart" /tr "%~dp0start.bat" /sc daily /st 09:10

:: Schedule stop.bat at 3:35 PM daily
schtasks /create /tn "AlgoTradingStop" /tr "%~dp0stop.bat" /sc daily /st 15:35

echo Tasks scheduled successfully.
pause