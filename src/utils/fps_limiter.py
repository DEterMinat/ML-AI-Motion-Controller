import time

class FPSLimiter:
    """
    FPS Limiter
    ===========
    Helps maintain a constant loop rate by sleeping the remaining time.
    Also provides FPS measurement.
    """
    
    def __init__(self, max_fps=30):
        """
        Initialize FPS Limiter
        
        Args:
            max_fps: Target FPS cap
        """
        self.max_fps = max_fps
        self.target_frame_time = 1.0 / max_fps
        self.last_frame_time = time.time()
        
        # FPS calculation
        self.start_time = time.time()
        self.frame_count = 0
        self.current_fps = 0.0
        self.fps_update_interval = 0.5 # Update FPS every 0.5s
        self.last_fps_update = time.time()
        
    def tick(self):
        """
        Call this at the end of the loop to limit FPS.
        """
        # Calculate how long the frame took
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        
        # Sleep if processing was faster than target frame time
        if elapsed < self.target_frame_time:
            time.sleep(self.target_frame_time - elapsed)
            
        # Update last frame time for next loop (after sleep)
        self.last_frame_time = time.time()
        
        # Update FPS counter
        self.frame_count += 1
        if current_time - self.last_fps_update > self.fps_update_interval:
            self.current_fps = self.frame_count / (current_time - self.last_fps_update)
            self.frame_count = 0
            self.last_fps_update = current_time
            
    def get_fps(self):
        """Get the current actual FPS"""
        return self.current_fps
