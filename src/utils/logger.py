import logging
import os
import sys

def setup_logger(name="MotionController"):
    """
    Sets up a centralized logger that outputs to both the console 
    and a rotating file in the logs/ directory.
    """
    # Create logs directory at project root
    # This assumes logger.py is in src/utils/
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "app.log")
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Formatter for log messages
        # Format: [2026-03-02 12:30:15] [INFO] [app.main] Log message...
        formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. File Handler (Rotating log file, append mode)
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO) # Save INFO and above to file
        file_handler.setFormatter(formatter)
        
        # 2. Console Handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO) # Adjust to DEBUG for more console output
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Create a default instance to be imported easily
app_logger = setup_logger()
