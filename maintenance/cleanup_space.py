import os
import shutil
import glob

def clean_project(root_dir):
    print(f"Cleaning temporary files in: {root_dir}")
    
    # 1. Clean __pycache__
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            if d == "__pycache__":
                path = os.path.join(root, d)
                try:
                    shutil.rmtree(path)
                    print(f"✓ Removed: {path}")
                except Exception as e:
                    print(f"❌ Failed to remove {path}: {e}")
            elif d == ".ipynb_checkpoints":
                 path = os.path.join(root, d)
                 try:
                    shutil.rmtree(path)
                    print(f"✓ Removed: {path}")
                 except Exception as e:
                    print(f"❌ Failed to remove {path}: {e}")
            elif d == ".pytest_cache":
                 path = os.path.join(root, d)
                 try:
                    shutil.rmtree(path)
                    print(f"✓ Removed: {path}")
                 except Exception as e:
                    print(f"❌ Failed to remove {path}: {e}")

    # 2. Check for large temp files (optional, be careful)
    # extensions_to_check = ['*.tmp', '*.log', '*.bak']
    # for ext in extensions_to_check:
    #     for file in glob.glob(os.path.join(root_dir, '**', ext), recursive=True):
    #         try:
    #             os.remove(file)
    #             print(f"✓ Removed file: {file}")
    #         except Exception as e:
    #             print(f"❌ Failed to remove {file}: {e}")

    print("\nCleanup complete!")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # Go up one level from scripts/
    clean_project(project_root)
