import time
import uasyncio as asyncio

import lightstate
import lightcontroller


class LightManager:

    def __init__(self):
        self.light_controller = lightcontroller.LightController()
        self.state = lightstate.ConstantLightState()
        
    def get_status(self):
        return {
            "level": self.light_controller.level,
            "state": self.state.state_type,
            "time_left": self.state.get_seconds_left(),
        }

    def constant(self, level: float):
        self.light_controller.set_level(level)
        self.state = lightstate.ConstantLightState()

    def fade(self, period: int, level: float):
        now_time = time.ticks_ms()
        now_level = self.light_controller.level
        then_time = time.ticks_add(now_time, int(period * 1000))
        self.state = lightstate.FadingLightState(now_time, now_level, then_time, level)

    def timer(self, period: int, level: float):
        now_time = time.ticks_ms()
        then_time = time.ticks_add(now_time, int(period * 1000))
        self.state = lightstate.TimerLightState(then_time, level)

    async def run(self):
        while True:
            self.run_timestep()
            await asyncio.sleep(0.1)

    def run_timestep(self):
        level = self.state.get_new_light_level()
        print(level)
        if level == "no change":
            return
        
        self.light_controller.set_level(level)
        if self.state.is_finished():
            print("finished")
            self.state = lightstate.ConstantLightState()        
        