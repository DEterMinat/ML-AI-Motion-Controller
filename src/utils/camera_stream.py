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
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            raise ValueError(f"Cannot open camera source: {src}")
            
        import src.config as config
        
        # Set resolution (optional, can be moved to config)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.stream.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        (self.grabbed, self.frame) = self.stream.read()
        
        self.name = name
        self.stopped = False
        self.frame_count = 0
        self.start_time = time.time()
        
    def start(self):
        """Start the thread to read frames from the video stream"""
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self
        
    def update(self):
        """Keep looping infinitely until the thread is stopped"""
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
