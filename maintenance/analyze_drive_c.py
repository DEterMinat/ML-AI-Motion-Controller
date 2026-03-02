import os
import heapq

def get_directory_size(directory):
    total_size = 0
    try:
        # Use scandir for faster traversal
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_file(follow_symlinks=False):
                    total_size += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                     # Recursive call might be too slow for C:\, so we might just do top-level logic in main
                     pass 
    except Exception:
        pass
    return total_size

def analyze_drive_c(top_n=20):
    root_path = "C:\\"
    print(f"🔍 Analyzing Drive C: (Skipping C:\\Windows for speed/safety)...")
    print(f"This might take a minute. Please wait...\n")

    # Store (size, path)
    large_files = []
    folder_sizes = {}
    
    # Directories to scan recursively (exclude Windows)
    scan_paths = [
        os.path.join(root_path, "Users"),
        os.path.join(root_path, "Program Files"),
        os.path.join(root_path, "Program Files (x86)"),
        os.path.join(root_path, "ProgramData"),
        # Add others if needed
    ]

    for start_path in scan_paths:
        if not os.path.exists(start_path): continue
        
        print(f"📂 Scanning: {start_path} ...")
        
        for root, dirs, files in os.walk(start_path):
            # Skip hidden/system folders that cause issues
            if "Windows" in root: continue
            
            curr_folder_size = 0
            
            for name in files:
                try:
                    filepath = os.path.join(root, name)
                    size = os.path.getsize(filepath)
                    curr_folder_size += size
                    
                    # Add to top files list
                    if len(large_files) < top_n:
                        heapq.heappush(large_files, (size, filepath))
                    else:
                        heapq.heappushpop(large_files, (size, filepath))
                        
                except Exception:
                    continue
            
            # Aggregate folder size (simplified for immediate folder consumption)
            # For a true tree map, we'd need to propagate up, but identifying heavy leaf nodes is often enough
            folder_sizes[root] = curr_folder_size

    # Sort and Print Results
    print("\n" + "="*50)
    print(f"📦 TOP {top_n} LARGEST FILES")
    print("="*50)
    
    # Sort descending
    sorted_files = sorted(large_files, key=lambda x: x[0], reverse=True)
    
    for size, path in sorted_files:
        size_gb = size / (1024**3)
        if size_gb >= 1.0:
            print(f"{size_gb:8.2f} GB  | {path}")
        else:
            size_mb = size / (1024**2)
            print(f"{size_mb:8.2f} MB  | {path}")

    print("\n" + "="*50)
    print(f"📂 TOP {top_n} HEAVY FOLDERS (Immediate Content)")
    print("="*50)
    
    sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)[:top_n]
    for path, size in sorted_folders:
        size_gb = size / (1024**3)
        if size_gb >= 1.0:
            print(f"{size_gb:8.2f} GB  | {path}")
        else:
             size_mb = size / (1024**2)
             print(f"{size_mb:8.2f} MB  | {path}")

if __name__ == "__main__":
    analyze_drive_c()
