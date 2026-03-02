
$vhdxPath = "C:\Users\tanak\AppData\Local\Docker\wsl\main\ext4.vhdx"
if (-not (Test-Path $vhdxPath)) {
    $vhdxPath = "$env:LOCALAPPDATA\Docker\wsl\data\ext4.vhdx"
}

if (Test-Path $vhdxPath) {
    Write-Host "✅ Found Docker VHDX at: $vhdxPath" -ForegroundColor Green
    Write-Host "`nTo reclaim space, run these commands in an ADMIN PowerShell:" -ForegroundColor Yellow
    Write-Host "1. wsl --shutdown"
    Write-Host "2. diskpart"
    Write-Host "`nThen inside diskpart, type:"
    Write-Host "   select vdisk file=`"$vhdxPath`"" -ForegroundColor Cyan
    Write-Host "   attach vdisk readonly" -ForegroundColor Cyan
    Write-Host "   compact vdisk" -ForegroundColor Cyan
    Write-Host "   detach vdisk" -ForegroundColor Cyan
    Write-Host "   exit" -ForegroundColor Cyan
}
else {
    Write-Host "❌ Could not find ext4.vhdx at standard locations." -ForegroundColor Red
    Write-Host "Please search for 'ext4.vhdx' on your C: drive manually."
}
