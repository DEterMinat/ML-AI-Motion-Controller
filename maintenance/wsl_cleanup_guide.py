import subprocess
import os

def wsl_deep_cleanup():
    print("🐳 WSL / Docker Deep Cleanup Guide")
    print("====================================")
    
    print("\n[STEP 1] Internal WSL Cleanup")
    print("Run these commands inside your WSL terminal (e.g., Ubuntu):")
    print("1. Clean Docker system:  docker system prune -a --volumes -f")
    print("2. Clean package cache:  sudo apt-get clean && sudo apt-get autoremove")
    print("3. Check large folders:  du -sh /var/lib/docker")

    print("\n[STEP 2] Shrink Docker VHDX (THE MOST IMPORTANT STEP)")
    print("Even after deleting files, Windows won't reclaim space automatically.")
    print("Perform these steps manually:")
    
    print("\n1. Right-click Docker icon in Taskbar -> Quit Docker Desktop.")
    print("2. Open PowerShell as Administrator and run:")
    print("   wsl --shutdown")
    
    print("\n3. Find your VHDX file. It is usually at:")
    print("   %LOCALAPPDATA%\\Docker\\wsl\\data\\ext4.vhdx")
    
    print("\n4. Create a file named 'compact.txt' with these lines:")
    print("   select vdisk file=\"C:\\Users\\YOUR_USER\\AppData\\Local\\Docker\\wsl\\data\\ext4.vhdx\"")
    print("   attach vdisk readonly")
    print("   compact vdisk")
    print("   detach vdisk")
    print("   exit")
    
    print("\n5. Run this command in CMD (as Admin):")
    print("   diskpart /s compact.txt")

    print("\n------------------------------------")
    print("I have generated a helper script 'scripts/shrink_docker.ps1' for you.")
    print("It will try to find the path and give you the exact diskpart commands.")

def create_ps_helper():
    ps_content = r'''
$vhdxPath = "$env:LOCALAPPDATA\Docker\wsl\data\ext4.vhdx"
if (-not (Test-Path $vhdxPath)) {
    $vhdxPath = "$env:USERPROFILE\AppData\Local\Docker\wsl\data\ext4.vhdx"
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
} else {
    Write-Host "❌ Could not find ext4.vhdx at standard locations." -ForegroundColor Red
    Write-Host "Please search for 'ext4.vhdx' on your C: drive manually."
}
'''
    with open("scripts/shrink_docker_helper.ps1", "w", encoding="utf-8") as f:
        f.write(ps_content)

if __name__ == "__main__":
    wsl_deep_cleanup()
    create_ps_helper()
