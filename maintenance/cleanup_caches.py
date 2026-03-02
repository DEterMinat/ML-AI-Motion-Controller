import shutil
import os
import sys

def clean_folder(path):
    if os.path.exists(path):
        try:
            print(f"Cleaning: {path} ...")
            # shutil.rmtree might fail on some files if they are in use, but usually okay for caches
            shutil.rmtree(path)
            print(f"✅ Deleted: {path}")
        except PermissionError:
             print(f"❌ Permission Denied: {path} (Try running as Administrator)")
        except Exception as e:
            print(f"❌ Failed to delete {path}: {e}")
    else:
        print(f"⚠️  Not found (already clean): {path}")

def cleanup_caches():
    print("🧹 Starting Cache Cleanup (NVIDIA & Driver Booster)...")
    
    targets = [
        # NVIDIA Installer/Update Cache
        r"C:\ProgramData\NVIDIA Corporation\NVIDIA App\UpdateFramework\ota-artifacts",
        r"C:\ProgramData\NVIDIA Corporation\Downloader",
        r"C:\ProgramData\NVIDIA Corporation\NetService",
        # NVIDIA Shader Cache (Safe to delete, will rebuild)
        r"C:\Users\tanak\AppData\Local\NVIDIA\DXCache",
        r"C:\Users\tanak\AppData\Local\NVIDIA\GLCache",
        
        # Driver Booster Downloads & Backups
        r"C:\ProgramData\IObit\Driver Booster\Download",
        r"C:\ProgramData\IObit\Driver Booster\Backups",
        r"C:\ProgramData\IObit\Driver Booster\Tmp"
    ]
    
    for path in targets:
        clean_folder(path)
    
    print("\n✨ Cleanup process finished.")

if __name__ == "__main__":
    cleanup_caches()
