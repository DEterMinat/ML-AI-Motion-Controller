import customtkinter as ctk
import asyncio
import websockets
import json
import threading
from ctypes import windll, c_int, byref, sizeof, Structure

# ==================== WIN32 TRANSPARENT WINDOW CONFIG ====================
# Constants for Windows API to make window click-through
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
LWA_ALPHA = 0x00000002

class RECT(Structure):
    _fields_ = [("left", c_int), ("top", c_int), ("right", c_int), ("bottom", c_int)]

class OverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Config
        self.title("ML-AI Motion Overlay")
        self.geometry("400x150")
        self.overrideredirect(True) # Remove title bar
        self.attributes("-topmost", True) # Keep on top
        self.attributes("-transparentcolor", "black") # Make black color transparent
        self.config(bg="black")

        # Setup UI
        self.setup_ui()
        
        # State
        self.running = True
        self.client_thread = None
        
        # Make Click-Through (Windows Only)
        self.after(500, self.make_click_through)
        
        # Start WebSocket Client
        self.start_client()
        
    def setup_ui(self):
        """Build the HUD interface"""
        self.frameless_drag = False # Disable drag since we want click-through
        
        # Container
        self.container = ctk.CTkFrame(self, fg_color="black", bg_color="black") # Black = Transparent
        self.container.pack(fill="both", expand=True)

        # Action Label (Big Text)
        self.action_label = ctk.CTkLabel(self.container, text="WAITING...", 
                                       font=("Impact", 40), text_color="#00FF00")
        self.action_label.pack(pady=(10, 0))
        
        # Confidence Bar
        self.progress = ctk.CTkProgressBar(self.container, width=300, height=15, progress_color="#00FF00")
        self.progress.set(0.0)
        self.progress.pack(pady=5)
        
        # Stats Label
        self.stats_label = ctk.CTkLabel(self.container, text="FPS: 00 | Conf: 0.00", 
                                      font=("Arial", 12), text_color="white")
        self.stats_label.pack()

    def make_click_through(self):
        """Use Win32 API to set WS_EX_TRANSPARENT"""
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            # 255 = Opaque (for the non-transparent parts), 0 = key to transparent color
            # We rely on -transparentcolor attribute of tkinter mostly, 
            # but EX_TRANSPARENT allows click-through.
            print("✓ Overlay Click-through Enabled")
        except Exception as e:
            print(f"⚠ Click-through Error: {e}")

    def update_hud(self, action, confidence):
        """Update UI from Main Thread"""
        # Determine Color
        color = "#00FF00" # Green
        if confidence < 0.5: color = "#FF0000" # Red
        elif confidence < 0.8: color = "#FFFF00" # Yellow
        
        self.action_label.configure(text=str(action).upper(), text_color=color)
        self.progress.configure(progress_color=color)
        self.progress.set(confidence)
        self.stats_label.configure(text=f"Conf: {confidence:.2f}")

    async def ws_client_loop(self):
        """WebSocket Client running asynchronously"""
        uri = "ws://localhost:8765"
        while self.running:
            try:
                # Update status
                self.stats_label.configure(text_color="gray", text="Connecting...")
                
                async with websockets.connect(uri) as websocket:
                    print(f"✓ Overlay Connected to {uri}")
                    self.stats_label.configure(text_color="white", text="Connected")
                    
                    while self.running:
                        try:
                            # Use wait_for to allow checking self.running periodically
                            msg = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                            data = json.loads(msg)
                            
                            # Check for Shutdown Signal
                            if data.get("event") == "shutdown":
                                print("✓ Server Shutdown received")
                                self.running = False
                                return

                            if "action" in data:
                                self.update_hud(data.get("action", "-"), data.get("confidence", 0.0))
                                
                        except asyncio.TimeoutError:
                            continue # Just check self.running again
                        except websockets.exceptions.ConnectionClosed:
                            print("⚠ Connection Closed")
                            break
                        except Exception as e:
                            print(f"⚠ Receive Error: {e}")
                            break
                            
            except (OSError, ConnectionRefusedError):
                self.stats_label.configure(text_color="red", text="No Server")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"⚠ Client Error: {e}")
                await asyncio.sleep(2)

    async def tkinter_loop(self):
        """Async loop to update the CustomTkinter UI"""
        while self.running:
            self.update() # Update UI
            await asyncio.sleep(0.02) # Yield control back to event loop (~50Hz update rate)
            
        self.destroy() # Close window when running becomes False

    async def run_app(self):
        """Run both loops concurrently"""
        await asyncio.gather(
            self.tkinter_loop(),
            self.ws_client_loop()
        )

def main():
    app = OverlayApp()
    try:
        asyncio.run(app.run_app())
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    main()
