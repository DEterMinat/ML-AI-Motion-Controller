from collections import deque
from collections import Counter
import time

class MotionAnalyzer:
    """
    Motion Analyzer
    ===============
    Analyzes a sequence of pose predictions to filter noise and detect distinct actions.
    
    Features:
    1. History Buffer: Looks at last N frames to smooth jitter.
    2. Consistency Check: Requires action to be detected in M frames to be valid.
    3. State Machine: Enforces "Neutral Reset" to prevent accidental double-hits.
    """
    
    def __init__(self, history_size=6, consistency_threshold=4, temporal_window=3):
        """
        Initialize Motion Analyzer
        
        Args:
            history_size: Number of frames to keep in buffer
            consistency_threshold: Minimum matching frames to confirm prediction
            temporal_window: Number of recent frames to use for temporal smoothing (voting)
        """
        self.history = deque(maxlen=history_size)
        self.consistency_threshold = consistency_threshold
        
        # Temporal Smoothing Buffer [NEW]
        self.prediction_buffer = deque(maxlen=temporal_window)
        
        self.state = "NEUTRAL"  # States: NEUTRAL, ACTION
        self.last_action = None
        self.cooldown_until = 0
        
    def process_prediction(self, label, confidence):
        """
        Process a new frame prediction with Temporal Smoothing.
        
        Returns:
            triggered_action: The action label if a new action is confirmed, else None.
            is_consistent: Boolean indicating if the input is stable.
        """
        # 1. Temporal Smoothing (Prediction Buffer)
        # Instead of deciding immediately, we buffer the raw labels
        raw_label = label if label is not None else "neutral"
        self.prediction_buffer.append(raw_label)
        
        # Wait until we have enough frames for smoothing
        if len(self.prediction_buffer) < self.prediction_buffer.maxlen:
            return None, False
            
        # Get the 'smoothed' label by majority vote over the temporal window
        counts = Counter(self.prediction_buffer)
        smoothed_label, _ = counts.most_common(1)[0]
        
        # 2. Add smoothed label to action history
        self.history.append(smoothed_label)
            
        # Wait until history is full-ish for consistency checking
        if len(self.history) < self.consistency_threshold:
            return None, False
            
        # 3. Get most frequent label in recent history for Consistency Checking
        hist_counts = Counter(self.history)
        most_common_label, count = hist_counts.most_common(1)[0]
        
        # 4. Check Consistency
        is_consistent = count >= self.consistency_threshold
        
        if not is_consistent:
            return None, False
            
        # RAW MODE BYPASS
        # If threshold is 1, we want instant response without state machine latching
        if self.consistency_threshold == 1:
            if most_common_label == "neutral":
                return None, True
            return most_common_label, True

        # 4. State Machine & Trigger Logic
        triggered_action = None
        
        if self.state == "NEUTRAL":
            if most_common_label != "neutral":
                # Transition to ACTION
                self.state = "ACTION"
                self.last_action = most_common_label
                triggered_action = most_common_label
                # print(f" [Analyzer] Triggered: {triggered_action}")
                
        elif self.state == "ACTION":
            # To reset to NEUTRAL, we need consistent 'neutral' or a DIFFERENT action
            # For strict boxing, usually we want to return to neutral before punching again.
            if most_common_label == "neutral":
                self.state = "NEUTRAL"
                self.last_action = None
                # print(" [Analyzer] Reset to Neutral")
            
            elif most_common_label != self.last_action:
                # Detected a different action without going fully neutral?
                # Depending on game, this might be a combo or just noise.
                # Let's switch state immediately for responsiveness.
                self.state = "ACTION"
                self.last_action = most_common_label
                triggered_action = most_common_label
                
        return triggered_action, is_consistent

    def reset(self):
        """Reset history and state"""
        self.history.clear()
        self.state = "NEUTRAL"
