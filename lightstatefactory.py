import time
import lightstate


class LightStateFactory:
    def create(self, time_now, level_now):
        raise Exception("not implemented")

    def to_dict(self):
        raise Exception("not implemented")


class ConstantLightStateFactory(LightStateFactory):
    def __init__(self, level):
        self.level = level

    def create(self, time_now, level_now):
        return lightstate.ConstantLightState(self.level)

    def to_dict(self):
        return {
            "type": lightstate.LIGHT_STATE_CONSTANT,
            "level": self.level,
        }


class FadingLightStateFactory(LightStateFactory):
    def __init__(self, seconds, level):
        self.end_level = level
        self.seconds = seconds

    def create(self, time_now, level_now):
        end_time = time.ticks_add(time_now, int(self.seconds * 1000))
        return lightstate.FadingLightState(
            time_now, level_now, end_time, self.end_level
        )

    def to_dict(self):
        return {
            "type": lightstate.LIGHT_STATE_FADING,
            "level": self.end_level,
            "seconds": self.seconds,
        }


class TimerLightStateFactory(LightStateFactory):
    def __init__(self, seconds, level):
        self.end_level = level
        self.seconds = seconds

    def create(self, time_now, level_now):
        end_time = time.ticks_add(time_now, int(self.seconds * 1000))
        return lightstate.TimerLightState(level_now, end_time, self.end_level)

    def to_dict(self):
        return {
            "type": lightstate.LIGHT_STATE_TIMER,
            "level": self.end_level,
            "seconds": self.period,
        }


class RaveLightStateFactory(LightStateFactory):
    def create(self, time_now, level_now):
        return lightstate.RaveLightState()

    def to_dict(self):
        return {
            "type": lightstate.LIGHT_STATE_RAVE,
        }


factory_lookup = {
    lightstate.LIGHT_STATE_CONSTANT: ConstantLightStateFactory,
    lightstate.LIGHT_STATE_FADING: FadingLightStateFactory,
    lightstate.LIGHT_STATE_TIMER: TimerLightStateFactory,
    lightstate.LIGHT_STATE_RAVE: RaveLightStateFactory,
}


def from_dict(info):
    factory = factory_lookup[info["type"]]
    del info["type"]
    return factory(**info)
