from machine import Pin
import uasyncio as asyncio

class Led:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)

    async def flash(self, interval=0.5):
        
        while True:
            self.led.toggle()
            await asyncio.sleep(interval)
        
    def set(self, value):
        self.led.value(value)
