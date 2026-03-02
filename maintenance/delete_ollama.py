import shutil
import os
import time

def delete_ollama_models():
    ollama_path = r"C:\Users\tanak\.ollama\models"
    
    if os.path.exists(ollama_path):
        print(f"🗑️  Found Ollama models at: {ollama_path}")
        print("Calculating size...")
        
        # Calculate size (optional but good for confirmation)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(ollama_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        
        size_gb = total_size / (1024**3)
        print(f"📦 Size to free: {size_gb:.2f} GB")
        
        print("Deleting... (This might take a moment)")
        try:
            shutil.rmtree(ollama_path)
            print("✅ Successfully deleted Ollama models.")
        except Exception as e:
            print(f"❌ Error deleting folder: {e}")
            print("Tip: If Ollama is running, please quit it from the taskbar first.")
    else:
        print("⚠️  Ollama models folder not found (already deleted?).")

if __name__ == "__main__":
    delete_ollama_models()
