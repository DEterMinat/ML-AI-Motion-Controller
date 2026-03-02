import shutil
import os

def check_c_drive_space():
    path = "C:/"
    try:
        total, used, free = shutil.disk_usage(path)
        
        # Convert to GB
        total_gb = total / (2**30)
        used_gb = used / (2**30)
        free_gb = free / (2**30)
        
        print(f"📊 Drive C: Status")
        print(f"-------------------")
        print(f"Total Space: {total_gb:.2f} GB")
        print(f"Used Space:  {used_gb:.2f} GB")
        print(f"Free Space:  {free_gb:.2f} GB")
        
        if free_gb < 1:
            print("\n⚠️  WARNING: Space is extremely low (less than 1GB)!")
        elif free_gb < 10:
            print("\n⚠️  Note: Space is better (~8-9GB), but aim for >20GB for safety.")
        else:
            print("\n✅ Space looks good.")
            
    except Exception as e:
        print(f"❌ Error checking disk space: {e}")

if __name__ == "__main__":
    check_c_drive_space()
