import os
import subprocess
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_compact():
    # List of VHDX files to check and compact
    vhdx_candidates = [
        r"C:\Users\tanak\AppData\Local\Docker\wsl\disk\docker_data.vhdx", # Found in deep scan (5.56 GB)
        r"C:\Users\tanak\AppData\Local\Docker\wsl\main\ext4.vhdx",       # Found previously
        r"C:\Users\tanak\AppData\Local\Docker\wsl\data\ext4.vhdx"        # Standard location
    ]
    
    found_vhdx = [p for p in vhdx_candidates if os.path.exists(p)]
    
    if not found_vhdx:
        print("❌ Error: Could not find any Docker VHDX files.")
        return

    print("🛑 Step 1: Shutting down WSL...")
    subprocess.run(["wsl", "--shutdown"], shell=True)
    
    script_path = "compact_script.txt"
    
    for vhdx_path in found_vhdx:
        print(f"\n⚙️  Processing: {vhdx_path}")
        # Create temporary diskpart script for this file
        diskpart_content = f"""select vdisk file="{vhdx_path}"
attach vdisk readonly
compact vdisk
detach vdisk
exit
"""
        with open(script_path, "w") as f:
            f.write(diskpart_content)
        
        try:
            # Run diskpart
            result = subprocess.run(["diskpart", "/s", script_path], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("✅ Compacted successfully!")
            else:
                print("⚠️ Diskpart issue. ensure you are admin.")
                print(result.stdout)
        except Exception as e:
            print(f"❌ Failed: {e}")

    # Cleanup script file
    if os.path.exists(script_path):
        os.remove(script_path)
    
    print("\n✅ All operations complete.")

if __name__ == "__main__":
    print("🥊 Docker VHDX Auto-Compactor")
    print("--------------------------------")
    
    if not is_admin():
        print("⚠️  Warning: Admin rights not detected. Commands might fail.")
        
    print("👉 IMPORTANT: Please ensure Docker Desktop is CLOSED (Quit).")
    # Automation mode: Skip input prompt if 'force' is passed or just run it as requested
    run_compact()
