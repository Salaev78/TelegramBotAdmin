from collections import defaultdict

import time



class FloodTracker:

    MAX_MESSAGES = 5
    TIME_WINDOW = 10
    
    def __init__(self):
        self.history = defaultdict(list)

    
    def register_message(self, user_id: int) -> bool:
        current_time = time.time()
        
        self.history[user_id].append(current_time)
        
        self.history[user_id] = [
            timestamp
            for timestamp in self.history[user_id]
            if current_time - timestamp <= self.TIME_WINDOW
        ]        
        
        if not self.history[user_id]:
            del self.history[user_id]
            return False
        
        if len(self.history[user_id]) >= self.MAX_MESSAGES:
            return True
        
        return False
        
        

flood_tracker = FloodTracker()