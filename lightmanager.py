import time
import uasyncio as asyncio
from machine import RTC

import lightstate
import lightstatefactory
import lightcontroller
import alarm


class LightManager:
    def __init__(self):
        self.light_controller = lightcontroller.LightController()
        self.state = lightstate.ConstantLightState(self.light_controller.level)
        self.alarms = alarm.AlarmManager()

    def get_status(self):
        return {
            "level": self.light_controller.level,
            "state": self.state.state_type,
            "time_left": self.state.get_seconds_left(),
        }

    def constant(self, level: float):
        self.set_state(lightstatefactory.ConstantLightStateFactory(level))

    def fade(self, period: int, level: float):
        self.set_state(lightstatefactory.FadingLightStateFactory(period, level))

    def timer(self, period: int, level: float):
        self.set_state(lightstatefactory.TimerLightStateFactory(period, level))

    def rave(self):
        self.set_state(lightstatefactory.RaveLightStateFactory())

    def set_state(self, factory):
        now_time = time.ticks_ms()
        self.state = factory.create(now_time, self.light_controller.level)

    async def run(self):
        while True:
            for _ in range(100):
                self.run_timestep()
                await asyncio.sleep(0.1)
            self.check_alarms()

    def run_timestep(self):
        level = self.state.get_light_level()
        self.light_controller.set_level(level)
        if self.state.is_finished():
            print("finished")
            self.state = lightstate.ConstantLightState(level)

    def check_alarms(self):
        datetime = RTC().datetime()
        date_now = datetime[:3]
        time_now = datetime[4:6]
        day_now = datetime[3]
        for alarm in self.alarms:
            if alarm.triggered(time_now, date_now, day_now):
                print("alarm triggered")
                self.state = alarm.state_factory.create(
                    time_now=time.ticks_ms(), level_now=self.light_controller.level
                )
                return
