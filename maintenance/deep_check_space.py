import subprocess
import os

def run_powershell(cmd):
    try:
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def deep_check():
    print("🔍 Starting Deep Drive C: Analysis...")
    print("--------------------------------------")
    
    # 1. Look for Top 10 Largest Files on C: (Top 20 excluding Windows)
    # This might take a bit of time but is very effective.
    print("\n📦 Top 20 Largest Files (excluding C:\\Windows):")
    file_check_cmd = (
        "Get-ChildItem -Path C:\\ -File -Recurse -ErrorAction SilentlyContinue | "
        "Where-Object { $_.FullName -notlike 'C:\\Windows*' } | "
        "Sort-Object Length -Descending | Select-Object -First 20 | "
        "Select-Object @{Name='Size(GB)';Expression={'{0:N2}' -f ($_.Length / 1GB)}}, FullName | Format-Table -AutoSize"
    )
    print(run_powershell(file_check_cmd))

    # 2. Check Size of current project dataset
    print("\n📂 Project Dataset Size:")
    # Get total size of 'dataset' folder in GB
    dataset_cmd = (
        "$size = (Get-ChildItem -Path . -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB; "
        "write-host ('Current Project Size: {0:N2} GB' -f $size)"
    )
    print(run_powershell(dataset_cmd))

    # 3. Check Trash/Recycle Bin Size
    print("\n🗑️  Recycle Bin Size:")
    recycle_cmd = (
        "$shell = New-Object -ComObject Shell.Application; "
        "$bin = $shell.Namespace(0x0a); "
        "$size = ($bin.Items() | Measure-Object -Property Size -Sum).Sum / 1GB; "
        "write-host ('Recycle Bin: {0:N2} GB' -f $size)"
    )
    print(run_powershell(recycle_cmd))

    print("\n--------------------------------------")
    print("💡 Advice: Look at the files above. High GB files are usually videos, installers (.exe/.msi), or caches.")

if __name__ == "__main__":
    # Ensure we are in project root for point #2
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    os.chdir(project_root)
    deep_check()
