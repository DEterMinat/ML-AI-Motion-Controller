# Check for Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "⚠️  Requesting Administrator Privileges to delete protected files..." -ForegroundColor Yellow
    $newProcess = Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs -PassThru
    exit
}

# --- We are now running as Administrator ---
$ErrorActionPreference = "SilentlyContinue"
Write-Host "🚀 STARTING ADMIN CLEANUP" -ForegroundColor Green
Write-Host "--------------------------------"

# 1. Clean Protected Caches
Write-Host "`n[1/3] 🔥 Force Cleaning Caches..."
$targets = @(
    "C:\ProgramData\NVIDIA Corporation\Downloader",
    "C:\ProgramData\NVIDIA Corporation\NVIDIA App\UpdateFramework\ota-artifacts",
    "C:\Users\tanak\AppData\Local\NVIDIA\DXCache",
    "C:\ProgramData\IObit\Driver Booster\Download",
    "C:\ProgramData\IObit\Driver Booster\Backups"
)

foreach ($path in $targets) {
    if (Test-Path $path) {
        Write-Host "   Deleting: $path"
        Remove-Item -Path $path -Recurse -Force
        if (Test-Path $path) { Write-Host "     ❌ Still exists (Locked by process)" -ForegroundColor Red }
        else { Write-Host "     ✅ Deleted" -ForegroundColor Cyan }
    }
}

# 2. Compact Docker VHDX
Write-Host "`n[2/3] 🐳 Compacting Docker VHDX..."
$vhdx_list = @(
    "C:\Users\tanak\AppData\Local\Docker\wsl\disk\docker_data.vhdx",
    "C:\Users\tanak\AppData\Local\Docker\wsl\main\ext4.vhdx"
)

# Shutdown WSL first
wsl --shutdown

foreach ($vhdx in $vhdx_list) {
    if (Test-Path $vhdx) {
        Write-Host "   Found: $vhdx"
        Write-Host "   Compacting... (This may take a moment)"
        
        $script = "select vdisk file=`"$vhdx`"`nattach vdisk readonly`ncompact vdisk`ndetach vdisk`nexit"
        $script | Out-File -Encoding ASCII "compact_tmp.txt"
        
        diskpart /s compact_tmp.txt | Out-Null
        Remove-Item "compact_tmp.txt"
        Write-Host "   ✅ Done" -ForegroundColor Cyan
    }
}

# 3. Final Check
Write-Host "`n[3/3] 📊 Final Space Check..."
Start-Sleep -Seconds 2
Get-Volume -DriveLetter C

Write-Host "`n✨ Cleanup Complete. You can close this window." -ForegroundColor Green
Read-Host "Press Enter to exit..."
