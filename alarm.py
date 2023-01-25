import random
from machine import RTC
import lightstatefactory


class Alarm:
    def __init__(self, time, state_factory, repeat, days):
        self.time = time
        self.state_factory = state_factory
        self.repeat = repeat
        self.days = days
        now = RTC().datetime()
        date_today = now[:3]
        time_now = now[4:6]
        self.last_triggered = None if time_now < self.time else date_today

    def triggered(self, time, date, day):
        if self.time > time:
            return False

        if self.days is not None and self.days[day] == 0:
            return False

        if self.last_triggered is not None and self.last_triggered >= date:
            return False

        self.last_triggered = date
        return True

    def to_dict(self):
        return {
            "time": list(self.time),
            "state": self.state_factory.to_dict(),
            "repeat": self.repeat,
            "days": self.days,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tuple(data["time"]),
            lightstatefactory.from_dict(data["state"]),
            data.get("repeat", False),
            data.get("days", None),
        )


class AlarmManager(list):
    def get_as_dicts(self):
        return [a.to_dict() for a in self]

    def add_from_dict(self, data):
        alarm = Alarm.from_dict(data)
        self.append(alarm)

    def update_from_dict(self, index, data):
        alarm = self[index]
        current_data = alarm.to_dict()
        current_data.update(data)
        self[index] = Alarm.from_dict(current_data)

    def check_for_triggered(self):
        datetime = RTC().datetime()
        date = datetime[:3]
        time = datetime[4:6]
        day = datetime[3]
        for alarm in self:
            if alarm.triggered(time, date, day):
                print("alarm triggered")
                return alarm
