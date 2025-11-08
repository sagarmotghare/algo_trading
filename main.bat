@echo off
setlocal EnableDelayedExpansion

:: === Flag Handling ===
if "%~1"=="--start" (
    call :show_banner
    call :activate_env
    call :log_env
    call :launch_python
    call :confirm_pid
    pause
    exit /b
) else if "%~1"=="--stop" (
    call :stop_process
    pause
    exit /b
) else if "%~1"=="--schedule" (
    call :schedule_tasks
    pause
    exit /b
) else if "%~1"=="--shortcut" (
    call :shortcut
    pause
    exit /b
) else (
    call :shortcut
    echo Usage:
    echo   main.bat --start     :: Launch AlgoTrading
    echo   main.bat --stop      :: Stop AlgoTrading
    echo   main.bat --schedule  :: Schedule daily start/stop tasks
    exit /b 1
)

:: === Function Definitions ===

:show_banner
echo ================================
echo           AlgoTrading           
echo ================================
echo An algorithmic trading system designed to train predictive models and operate on live market data.
echo.
exit /b

:activate_env
if exist ".venv\" (
    call .venv\Scripts\activate.bat
    echo Activated virtual environment.
) else (
    echo Virtual environment not found. Using global environment.
)
echo.
exit /b

:log_env
echo Python version:
python --version
echo Python path:
where python
echo.
exit /b

:launch_python
if not exist live.py (
    echo ERROR: live.py not found. Aborting launch.
    exit /b 1
)
powershell -Command "Start-Process python -ArgumentList 'live.py' -PassThru | Select-Object -ExpandProperty Id |  Out-File -Encoding ASCII -NoNewline pid.txt"
exit /b

:confirm_pid
:: Read timestamp (line 1)
set /p TS=<pid.txt

:: Read PID (line 2)
for /f "skip=1 delims=" %%i in (pid.txt) do (
    set PID=%%i
    goto :got_pid
)

:got_pid
echo Python PID: !PID!
echo Launched at: !TS!
echo PID and timestamp saved to pid.txt
echo.
exit /b

:stop_process
:: Read PID (line 2)
set /p RAW_PID=<pid.txt
for /f %%i in ("%RAW_PID%") do set PID=%%i

:kill_pid
echo Killing process with PID: !PID!
taskkill /PID !PID! /F
exit /b

:schedule_tasks
echo Scheduling AlgoTrading tasks...

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -ArgumentList '--schedule' -Verb runAs"
    exit /b
)

:: Schedule start.bat at 9:10 AM daily
schtasks /create /tn "AlgoTradingStart" /tr "%~dp0start.bat" /sc daily /st 09:10

:: Schedule stop.bat at 3:35 PM daily
schtasks /create /tn "AlgoTradingStop" /tr "%~dp0stop.bat" /sc daily /st 15:35

echo Tasks scheduled successfully.
exit /b

:shortcut
setlocal

:: Define paths
set TARGET_BATCH=%~dp0main.bat
set WORKING_DIR=%~dp0

:: Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%~dp0/StartAlgoTrading.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/c \"%TARGET_BATCH% --start\"'; $Shortcut.WorkingDirectory = '%WORKING_DIR%'; $Shortcut.IconLocation = 'cmd.exe'; $Shortcut.Save()"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%~dp0/StopAlgoTrading.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/c \"%TARGET_BATCH% --stop\"'; $Shortcut.WorkingDirectory = '%WORKING_DIR%'; $Shortcut.IconLocation = 'cmd.exe'; $Shortcut.Save()"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%~dp0/ScheduleAlgoTrading.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/c \"%TARGET_BATCH% --schedule\"'; $Shortcut.WorkingDirectory = '%WORKING_DIR%'; $Shortcut.IconLocation = 'cmd.exe'; $Shortcut.Save()"

endlocal