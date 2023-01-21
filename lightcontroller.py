from machine import Pin, PWM

DUTY_MAX = 65536

class LightController:

    def __init__(self):
        self.pin = Pin(13)
        self.pwm = PWM(self.pin)
        
    def get_level(self):
        return self.pwm.duty_u16() / DUTY_MAX

    def is_on(self):
        return self.pwm.duty_u16() != 0

    def set_level(self, percentage):
        if percentage == 1:
            self.gpio.write(PIN, 1)
        elif percentage == 0:
            self.gpio.write(PIN, 0)
        else:
            value = 2 + round(percentage * percentage * (DUTY_MAX-1))
            self.gpio.duty_u16(value)