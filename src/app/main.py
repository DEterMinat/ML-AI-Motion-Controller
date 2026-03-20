"""
Modern GUI Application for Motion Controller
============================================
Powered by customtkinter and Pillow.
Allows visual configuration and camera monitoring.
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import time
import os
import sys
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.game_engine import GameControllerThreaded
from utils.logger import app_logger
import config

# Set theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MotionControllerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.title("ML-AI Motion Controller v2.0")
        self.geometry("1100x700")
        
        # Initialize Game Controller
        self.controller = GameControllerThreaded()
        self.is_running = False
        self.image_tk = None
        self.overlay_process = None # Track overlay process

        # Layout Config
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_main_area()
        
        # Close Handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)


    # ... (Omitted methods for brevity) ...

        
    def create_sidebar(self):
        """Create left sidebar with controls"""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)
        
        # Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AI Controller", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Start/Stop Button
        self.start_btn = ctk.CTkButton(self.sidebar, text="Start Camera", command=self.toggle_camera, 
                                     fg_color="green", hover_color="darkgreen")
        self.start_btn.grid(row=1, column=0, padx=20, pady=10)
        
        # Calibrate Button
        self.cal_btn = ctk.CTkButton(self.sidebar, text="re-Calibrate (C)", command=self.calibrate,
                                   state="disabled")
        self.cal_btn.grid(row=2, column=0, padx=20, pady=10)
        
        # Separator
        ctk.CTkLabel(self.sidebar, text="Settings", font=ctk.CTkFont(size=16)).grid(row=3, column=0, pady=(20,0))
        
        # Confidence Slider
        self.conf_label = ctk.CTkLabel(self.sidebar, text=f"Confidence: {config.CONFIDENCE_THRESHOLD}")
        self.conf_label.grid(row=4, column=0, padx=20, pady=(10,0))
        
        self.conf_slider = ctk.CTkSlider(self.sidebar, from_=0.1, to=1.0, number_of_steps=9, command=self.update_conf)
        self.conf_slider.set(config.CONFIDENCE_THRESHOLD)
        self.conf_slider.grid(row=5, column=0, padx=20, pady=(0,10))
        
        # Cooldown Slider (Simulated for now, as cooldown is in InputHandler)
        self.cool_label = ctk.CTkLabel(self.sidebar, text=f"Cooldown: {config.ACTION_COOLDOWN}s")
        self.cool_label.grid(row=6, column=0, padx=20, pady=(10,0))
        
        self.cool_slider = ctk.CTkSlider(self.sidebar, from_=0.1, to=2.0, number_of_steps=19, command=self.update_cool)
        self.cool_slider.set(config.ACTION_COOLDOWN)
        self.cool_slider.grid(row=7, column=0, padx=20, pady=(0,10))
        
        # Profile Settings Button [NEW]
        self.settings_btn = ctk.CTkButton(self.sidebar, text="Settings / Profiles", command=self.open_settings,
                                       fg_color="#0055AA", hover_color="#004488")
        self.settings_btn.grid(row=8, column=0, padx=20, pady=10)
        
        # Status
        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Stopped", text_color="gray")
        self.status_label.grid(row=9, column=0, padx=20, pady=10)

        # Overlay Button
        self.overlay_btn = ctk.CTkButton(self.sidebar, text="Open Overlay (HUD)", command=self.launch_overlay,
                                       fg_color="#555555", hover_color="#777777")
        self.overlay_btn.grid(row=10, column=0, padx=20, pady=20)
        
    def open_settings(self):
        """Open the Profile & Settings UI"""
        from app.profiles_ui import SettingsUI
        
        def on_bindings_changed(new_bindings):
            # Update the game controller with new bindings
            if hasattr(self, 'controller'):
                self.controller.update_bindings(new_bindings)
                
        # Create and show the settings window
        SettingsUI(self, on_profile_changed_callback=on_bindings_changed)

    def launch_overlay(self):
        """Launch the transparent overlay process"""
        try:
            # Use sys.executable to ensure we use the same venv python
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overlay.py")
            subprocess.Popen([sys.executable, script_path])
            app_logger.info("Overlay Launched")
        except Exception as e:
            app_logger.error(f"Failed to launch overlay: {e}")

    def create_main_area(self):
        """Create main area for camera feed"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Image Display
        self.image_label = ctk.CTkLabel(self.main_frame, text="Camera Off\nPress Start to Begin", 
                                      font=ctk.CTkFont(size=20))
        self.image_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Info Bar
        self.info_bar = ctk.CTkLabel(self.main_frame, text="Prediction: - | Action: -", 
                                   font=ctk.CTkFont(size=14))
        self.info_bar.grid(row=1, column=0, pady=10, sticky="ew")

    def toggle_camera(self):
        if not self.is_running:
            # Start
            self.controller.start()
            self.is_running = True
            
            self.start_btn.configure(text="Stop Camera", fg_color="red", hover_color="darkred")
            self.cal_btn.configure(state="normal")
            self.status_label.configure(text="Status: Running", text_color="green")
            
            # Start Loop
            self.update_frame()
        else:
            # Stop
            self.is_running = False
            self.controller.stop()
            
            self.start_btn.configure(text="Start Camera", fg_color="green", hover_color="darkgreen")
            self.cal_btn.configure(state="disabled")
            self.status_label.configure(text="Status: Stopped", text_color="gray")
            
            self.image_label.configure(image=None, text="Camera Off")

    def calibrate(self):
        if self.is_running:
            self.controller.analyzer.reset()
            self.status_label.configure(text="Status: Calibrated!")
            self.after(1000, lambda: self.status_label.configure(text="Status: Running"))

    def update_conf(self, value):
        config.CONFIDENCE_THRESHOLD = round(value, 2)
        self.conf_label.configure(text=f"Confidence: {config.CONFIDENCE_THRESHOLD}")
        
    def update_cool(self, value):
        # Note: changing config vars like this works for direct reads, 
        # but InputHandler might need manual update if it cached value.
        # For v2, let's assume simple config read is enough or update handler map
        config.ACTION_COOLDOWN = round(value, 1)
        self.controller.input_handler.cooldown_duration = config.ACTION_COOLDOWN
        self.cool_label.configure(text=f"Cooldown: {config.ACTION_COOLDOWN}s")

    def update_frame(self):
        """Main loop callback"""
        if not self.is_running:
            return
            
        # Process frame
        try:
            frame, stats = self.controller.process_frame()
        except Exception as e:
            app_logger.error(f"Update Error: {e}")
            self.after(100, self.update_frame) # Retry slowly
            return
        
        if frame is not None:
            # Convert Color: BGR (OpenCV) -> RGB (Pillow)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Explicitly resize using OpenCV to avoid Pillow/Tkinter memory stride distortion 
            frame_resized = cv2.resize(frame_rgb, (640, 480))
            img = Image.fromarray(frame_resized)
            
            # Create CTkImage
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
            
            # Update Label
            self.image_label.configure(image=ctk_img, text="")
            self.image_tk = ctk_img # Keep reference
            
            # Update Info
            if stats:
                pred = stats['prediction'] or "-"
                act = stats['action'] or "-"
                fps = stats['fps_app']
                self.info_bar.configure(text=f"Prediction: {pred} | Action: {act} | FPS: {fps:.1f}")

        # Schedule next update (10ms ~ 100 FPS cap for GUI, Logic capped internally)
        self.after(10, self.update_frame)

    def on_close(self):
        """Cleanup on close"""
        # 1. Send Shutdown Signal to Overlay
        try:
            if hasattr(self, 'controller') and self.controller.ws_server:
                self.controller.ws_server.broadcast({"event": "shutdown"})
                time.sleep(0.1) # Give time to send
        except:
            pass
            
        # 2. Stop Game Engine
        if self.is_running:
            self.controller.stop()
            
        # 3. Kill Overlay Forcefully (Backup)
        if self.overlay_process and self.overlay_process.poll() is None:
            try:
                self.overlay_process.terminate()
            except: pass
            
        self.destroy()

if __name__ == "__main__":
    app = MotionControllerApp()
    app.mainloop()
