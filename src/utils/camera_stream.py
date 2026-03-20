import cv2
from threading import Thread
import time

class CameraStream:
    """
    Threaded Camera Stream
    ======================
    Captures frames in a separate thread to prevent IO blocking.
    Always provides the most recent frame available.
    """
    
    def __init__(self, src=0, name="CameraStream"):
        """
        Initialize the camera stream
        
        Args:
            src: Camera source (default: 0 for webcam)
            name: Thread name
        """
        self.src = src
        self.name = name
        self.stopped = False
        self.frame_count = 0
        self.start_time = time.time()
        self.grabbed = False
        self.frame = None
        self.stream = None
        
    def start(self):
        """Start the thread to read frames from the video stream"""
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        
        # Wait up to 3 seconds for the first frame to populate
        timeout = time.time() + 3.0
        while not self.grabbed and not self.stopped and time.time() < timeout:
            time.sleep(0.05)
            
        return self
        
    def update(self):
        """Keep looping infinitely until the thread is stopped"""
        import os
        import src.config as config
        
        backend = cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY
        self.stream = cv2.VideoCapture(self.src, backend)
        
        if not self.stream.isOpened():
            print(f"[ERROR] Cannot open camera source: {self.src}")
            self.stopped = True
            return

        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.stream.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        self.start_time = time.time()

        while True:
            # If the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                return
                
            # Otherwise, read the next frame from the stream
            (grabbed, frame) = self.stream.read()
            
            # Update only if grabbed successfully
            if grabbed:
                self.grabbed = grabbed
                self.frame = frame
                self.frame_count += 1
            else:
                # If cannot grab, maybe stream ended or disconnected
                self.stopped = True
                self.stream.release()
                return
                
    def read(self):
        """Return the most recently read frame"""
        return self.frame
        
    def stop(self):
        """Indicate that the thread should be stopped"""
        self.stopped = True
        
    def get_fps(self):
        """Calculate and return average internal FPS"""
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            return self.frame_count / elapsed
        return 0.0
