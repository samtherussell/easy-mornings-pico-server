import random
from machine import RTC
import lightstatefactory


class Alarm:
    def __init__(self, enabled, time, state_factory, repeat, days):
        self.enabled = enabled
        self.time = time
        self.state_factory = state_factory
        self.repeat = repeat
        if days is not None and len(days) != 7:
            raise ValueError("days must be array of length 7")
        if any(x not in (True, False) for x in days):
            raise ValueError("days must be array of bools")
        self.days = days
        now = RTC().datetime()
        date_today = now[:3]
        time_now = now[4:6]
        self.last_triggered = None if time_now < self.time else date_today

    def triggered(self, time, date, day):
        if not self.enabled:
            return False

        if self.time > time:
            return False

        if self.days is not None and not self.days[day]:
            return False

        if self.last_triggered is not None and self.last_triggered >= date:
            return False

        self.last_triggered = date
        if not self.repeat:
            self.enabled = False
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
            enabled=data.get("enabled", True),
            time=tuple(data["time"]),
            state_factory=lightstatefactory.from_dict(data["state"]),
            repeat=data.get("repeat", False),
            days=data.get("days", None),
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
