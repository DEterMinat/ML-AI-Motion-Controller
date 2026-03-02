import subprocess
import sys

def run_command(command):
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

def cleanup_docker():
    print("🚀 Starting Docker Cleanup...")
    
    # 1. Check if docker is available
    try:
        subprocess.run("docker --version", shell=True, check=True, capture_output=True)
    except:
        print("❌ Docker is not installed or not in PATH.")
        return

    # 2. Prune everything (Containers, Images, Networks)
    # -a: Remove all unused images, not just dangling ones
    # --volumes: remove unused volumes
    # -f: Force/Do not prompt for confirmation
    print("\nRemoving unused containers, images, and networks...")
    run_command("docker system prune -a --volumes -f")

    print("\n✅ Docker cleanup complete!")
    print("Note: If using Docker Desktop on Windows, the .vhdx file may not shrink immediately.")

if __name__ == "__main__":
    cleanup_docker()
