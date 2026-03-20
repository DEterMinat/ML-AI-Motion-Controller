"""
Input Handler Utility
======================
Handles keyboard input simulation for game control
"""

import pydirectinput
import time

class InputHandler:
    """Handles keyboard input for game control"""
    
    def __init__(self, cooldown_duration=0.5):
        """
        Initialize input handler
        
        Args:
            cooldown_duration: Minimum time (seconds) between input actions
        """
        self.cooldown_duration = cooldown_duration
        self.last_action_time = {}
        self.held_keys = set()
        
        # Configure pydirectinput
        pydirectinput.FAILSAFE = False
        pydirectinput.PAUSE = 0.05
    
    def can_perform_action(self, action_name):
        """
        Check if enough time has passed since last action
        
        Args:
            action_name: Name of the action to check
            
        Returns:
            True if action can be performed, False otherwise
        """
        current_time = time.time()
        
        if action_name not in self.last_action_time:
            return True
        
        time_since_last = current_time - self.last_action_time[action_name]
        return time_since_last >= self.cooldown_duration

    def handle_hold(self, key, is_active):
        """
        Handle continuous key holding (e.g. Blocking)
        
        Args:
            key: Key to hold
            is_active: True to hold down, False to release
        """
        try:
            if is_active:
                if key not in self.held_keys:
                    pydirectinput.keyDown(key)
                    self.held_keys.add(key)
                    return True # Started holding
            else:
                if key in self.held_keys:
                    pydirectinput.keyUp(key)
                    self.held_keys.discard(key)
                    return False # Released
        except Exception as e:
            print(f"Error handling hold '{key}': {e}")
            return False
            
    def release_all(self):
        """Release all held keys"""
        for key in list(self.held_keys):
            try:
                pydirectinput.keyUp(key)
            except: pass
        self.held_keys.clear()

    def press_key(self, key, action_name=None):
        """
        Press a keyboard key, mouse click, or key combination with cooldown
        
        Args:
            key: Key string, list of keys, or 'click_left'/'click_right'
            action_name: Optional action name for cooldown tracking
            
        Returns:
            True if action was performed, False if on cooldown
        """
        if action_name is None:
            action_name = str(key)
        
        if not self.can_perform_action(action_name):
            return False
        
        try:
            # Handle Mouse Clicks
            if key in ['click_left', 'lclick', 'mouse_left', 'คลิ๊กซ้าย', 'คลิกซ้าย']:
                pydirectinput.click()
            elif key in ['click_right', 'rclick', 'mouse_right', 'คลิ๊กขวา', 'คลิกขวา']:
                pydirectinput.click(button='right')
            
            # Handle Key Combinations (List)
            elif isinstance(key, list):
                for k in key:
                    pydirectinput.keyDown(k)
                time.sleep(0.05)
                for k in reversed(key):
                    pydirectinput.keyUp(k)
            
            # Handle Single Key (With safety duration for games like Roblox)
            else:
                pydirectinput.keyDown(key)
                time.sleep(0.03)
                pydirectinput.keyUp(key)
                
            self.last_action_time[action_name] = time.time()
            return True
            
        except Exception as e:
            print(f"Error performing action '{key}': {e}")
            return False
    
    def press_key_combination(self, keys, action_name):
        """
        Press multiple keys simultaneously
        
        Args:
            keys: List of keys to press together
            action_name: Action name for cooldown tracking
            
        Returns:
            True if keys were pressed, False if on cooldown
        """
        if not self.can_perform_action(action_name):
            return False
        
        try:
            for key in keys:
                pydirectinput.keyDown(key)
            
            time.sleep(0.05)
            
            for key in reversed(keys):
                pydirectinput.keyUp(key)
            
            self.last_action_time[action_name] = time.time()
            return True
        except Exception as e:
            print(f"Error pressing key combination {keys}: {e}")
            return False
    
    def reset_cooldown(self, action_name=None):
        """
        Reset cooldown for specific action or all actions
        
        Args:
            action_name: Optional specific action to reset (None = reset all)
        """
        if action_name is None:
            self.last_action_time.clear()
        elif action_name in self.last_action_time:
            del self.last_action_time[action_name]
