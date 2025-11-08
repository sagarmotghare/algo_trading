@echo off
setlocal

:: Read and clean PID from pid.txt
set /p RAW_PID=<pid.txt
for /f %%i in ("%RAW_PID%") do set PID=%%i

echo Killing process with PID: %PID%
taskkill /PID %PID% /F

endlocal
pause