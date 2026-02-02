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
    
    def __init__(self, history_size=6, consistency_threshold=4):
        """
        Initialize Motion Analyzer
        
        Args:
            history_size: Number of frames to keep in buffer
            consistency_threshold: Minimum matching frames to confirm prediction
        """
        self.history = deque(maxlen=history_size)
        self.consistency_threshold = consistency_threshold
        
        self.state = "NEUTRAL"  # States: NEUTRAL, ACTION
        self.last_action = None
        self.cooldown_until = 0
        
    def process_prediction(self, label, confidence):
        """
        Process a new frame prediction.
        
        Returns:
            triggered_action: The action label if a new action is confirmed, else None.
            is_consistent: Boolean indicating if the input is stable.
        """
        # 1. Add to history (ignore None/Low confidence inputs if you want, 
        # or treat them as 'unknown' to break streaks. Here we treat None as 'neutral' or break)
        if label is None:
            self.history.append("neutral")
        else:
            self.history.append(label)
            
        # Wait until history is full-ish
        if len(self.history) < self.consistency_threshold:
            return None, False
            
        # 2. Get most frequent label in recent history (Smoothing)
        counts = Counter(self.history)
        most_common_label, count = counts.most_common(1)[0]
        
        # 3. Check Consistency
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
