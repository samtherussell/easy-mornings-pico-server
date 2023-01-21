from machine import Pin, PWM

DUTY_MAX = 65536

class LightController:

    def __init__(self):
        self.pin = Pin(13, mode=Pin.OUT)
        self.level = 0
        self.pin.value(self.level)
        self.pwm = None

    def set_level(self, percentage):
        self.level = percentage
        if percentage in [0, 1]:
            if self.pwm is not None:
                self.pwm = None
                self.pin.init(Pin.OUT)
            self.pin.value(percentage)
        else:
            if self.pwm is None:
                self.pin.init(Pin.ALT)
                self.pwm = PWM(self.pin)
            value = 2 + round(percentage * percentage * (DUTY_MAX-1))
            self.pwm.duty_u16(value)