$currentPath = (Get-Location).Path
$scriptPath  = Join-Path $currentPath "run.ps1"

# Debug: print current user and folder
Write-Host "Running as user: $env:UserName"
Write-Host "Current folder: $currentPath"
Write-Host "Script path: $scriptPath"

# Debug: check if elevated
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
Write-Host "Is elevated: $isAdmin"

if(-not $isAdmin) {
Start-Process -FilePath powershell.exe `
    -ArgumentList "-ExecutionPolicy Bypass -File $scriptPath -Command Set-Location `"$currentPath`"" `
    -Verb RunAs
}

powershell.exe

# Task name and folder
$taskName    = "Fetch Data"
$taskFolder  = "\AlgoTrading"

# Resolve current folder and script path
$scriptPath  = Join-Path $currentPath "run.ps1"

# Define the action (run PowerShell with your script, starting in current folder)
$taskAction  = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $currentPath

# Define the trigger (daily at 9 AM)
$taskTrigger = New-ScheduledTaskTrigger -Daily -At 9am

# Run under your account with highest privileges
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "SYSTEM"`
    -LogonType ServiceAccount `
    -RunLevel Highest

Write-Host "Running as user: $env:UserName"

# Register the task inside the AlgoTrading folder
Register-ScheduledTask -TaskName $taskName `
    -TaskPath $taskFolder `
    -Action $taskAction `
    -Trigger $taskTrigger `
    -Principal $taskPrincipal `
    -Description "Runs run.ps1 daily at 9 AM for AlgoTrading data fetch"

Write-Host "Task $taskFolder/$taskName is created." 