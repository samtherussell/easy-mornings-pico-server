import time

LIGHT_STATE_CONSTANT = 'LIGHT_STATE_CONSTANT'
LIGHT_STATE_FADING = 'LIGHT_STATE_FADING'
LIGHT_STATE_TIMER = 'LIGHT_STATE_TIMER'


class LightState:
    
    def __init__(self, state_type):
        self.state_type = state_type
    
    def get_new_light_level(self):
        return "no change"
    
    def get_seconds_left(self):
        raise Exception("not implemented")
    
    def is_finished(self):
        raise Exception("not implemented")
    

class ConstantLightState(LightState):
    
    def __init__(self):
        super().__init__(LIGHT_STATE_CONSTANT)
    
    def get_seconds_left(self):
        return -1
    
    def is_finished(self):
        return False

    
class FadingLightState(LightState):
    
    def __init__(self, start_time, start_level, end_time, end_level):
        super().__init__(LIGHT_STATE_FADING)
        self.start_time = start_time
        self.start_level = start_level
        self.end_time = end_time
        self.end_level = end_level
        
    def get_new_light_level(self):
        now = time.ticks_ms()
        progress = time.ticks_diff(now, self.start_time) / time.ticks_diff(self.end_time, self.start_time)
        if progress < 0:
            progress = 0
        elif progress > 1:
            progress = 1
        else:
            progress = round(progress, 2)
        level = self.start_level + progress * (self.end_level - self.start_level)
        return level

    def get_seconds_left(self):
        now = time.ticks_ms()
        return time.ticks_diff(self.end_time, now) // 1000
    
    def is_finished(self):
        return self.get_seconds_left() < 0


class TimerLightState(LightState):
    
    def __init__(self, time, level):
        super().__init__(LIGHT_STATE_TIMER)
        self.time = time
        self.level = level
        
    def get_new_light_level(self):
        if self.is_finished():
            return self.level
        else:
            return super().get_new_light_level()

    def get_seconds_left(self):
        now = time.ticks_ms()
        return time.ticks_diff(self.time, now) // 1000
    
    def is_finished(self):
        return self.get_seconds_left() < 0