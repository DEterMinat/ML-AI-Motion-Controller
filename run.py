"""
ML-AI Motion Controller Launcher
================================
Run this script to start the application.

Usage:
    python run.py
"""

import sys
import os

# Ensure the src directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import datetime
import traceback

# Global Exception Handler
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_msg = f"\n[{timestamp}] CRITICAL ERROR:\n{exc_value}\n"
    print(error_msg)
    
    with open("crash_log.txt", "a") as f:
        f.write(error_msg)
        traceback.print_tb(exc_traceback, file=f)
        f.write("\n" + "-"*50 + "\n")
        
    print("❌ An error occurred! Logs saved to crash_log.txt")

sys.excepthook = handle_exception

try:
    from src.app.main import MotionControllerApp
except ImportError:
    # Fallback if run directly from within src (unlikely but safe)
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    from src.app.main import MotionControllerApp

if __name__ == "__main__":
    print("🚀 Starting ML-AI Motion Controller...")
    app = MotionControllerApp()
    app.mainloop()
