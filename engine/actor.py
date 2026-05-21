import time

class Actor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.idle_down = []
        self.idle_up = []
        self.idle_left = []
        self.idle_right = []
        self.frames_left = []
        self.frames_right = []
        self.frames_top = []
        self.frames_bottom = []
        
        self.orientation = (0, 1) 
        
        self.last_x = x
        self.last_y = y
        self.is_moving = False
        
        self.current_frame_index = 0
        self.animation_speed = 0.15
        self.last_frame_time = time.time()

    def _update_movement_state(self):
        dx = self.x - self.last_x
        dy = self.y - self.last_y
        
        if abs(dx) > 0.001 or abs(dy) > 0.001:
            self.is_moving = True
            if abs(dx) > abs(dy):
                self.orientation = (-1, 0) if dx < 0 else (1, 0)
            else:
                self.orientation = (0, -1) if dy < 0 else (0, 1)
        else:
            self.is_moving = False
            
        self.last_x = self.x
        self.last_y = self.y

    def get_current_frame(self):
        self._update_movement_state()
        
        if self.is_moving:
            now = time.time()
            if now - self.last_frame_time > self.animation_speed:
                self.current_frame_index += 1
                self.last_frame_time = now

        frames = []
        idles = []
        
        if self.orientation == (-1, 0):
            frames = self.frames_left
            idles = self.idle_left
        elif self.orientation == (1, 0):
            frames = self.frames_right
            idles = self.idle_right
        elif self.orientation == (0, -1):
            frames = self.frames_top
            idles = self.idle_up
        elif self.orientation == (0, 1):
            frames = self.frames_bottom
            idles = self.idle_down

        if not self.is_moving:
            self.current_frame_index = 0
            if idles:
                return idles[0]
            if frames:
                return frames[0]
            return None

        if frames:
            return frames[self.current_frame_index % len(frames)]
        if idles:
            return idles[0]
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass