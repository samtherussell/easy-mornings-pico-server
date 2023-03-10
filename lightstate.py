import time

LIGHT_STATE_CONSTANT = "LIGHT_STATE_CONSTANT"
LIGHT_STATE_FADING = "LIGHT_STATE_FADING"
LIGHT_STATE_TIMER = "LIGHT_STATE_TIMER"
LIGHT_STATE_RAVE = "LIGHT_STATE_RAVE"


class LightState:
    def __init__(self, state_type):
        self.state_type = state_type

    def get_light_level(self):
        raise Exception("not implemented")

    def get_seconds_left(self):
        raise Exception("not implemented")

    def is_finished(self):
        raise Exception("not implemented")


class ConstantLightState(LightState):
    def __init__(self, level):
        super().__init__(LIGHT_STATE_CONSTANT)
        self.level = level

    def get_light_level(self):
        return self.level

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

    def get_light_level(self):
        now = time.ticks_ms()
        progress = time.ticks_diff(now, self.start_time) / time.ticks_diff(
            self.end_time, self.start_time
        )
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
    def __init__(self, start_level, end_time, end_level):
        super().__init__(LIGHT_STATE_TIMER)
        self.start_level = start_level
        self.end_time = end_time
        self.end_level = end_level

    def get_light_level(self):
        if self.is_finished():
            return self.end_level
        else:
            return self.start_level

    def get_seconds_left(self):
        now = time.ticks_ms()
        return time.ticks_diff(self.end_time, now) // 1000

    def is_finished(self):
        return self.get_seconds_left() < 0


class RaveLightState(LightState):

    wavelength = 250

    def __init__(self):
        super().__init__(LIGHT_STATE_RAVE)

    def get_light_level(self):
        now = time.ticks_ms()
        if now % self.wavelength < self.wavelength // 2:
            return 1
        else:
            return 0

    def get_seconds_left(self):
        return -1

    def is_finished(self):
        return False
