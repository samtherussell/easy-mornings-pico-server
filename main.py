import uasyncio as asyncio

from handler import EasyMorningHandler
from lightmanager import LightManager
from led import Led
import wifi


def main():
    asyncio.run(async_main())


async def async_main():

    await connect_to_wifi()

    light_manager = LightManager()
    handler = EasyMorningHandler(light_manager)
    asyncio.create_task(
        asyncio.start_server(handler.handle_connection, "0.0.0.0", 8080)
    )
    await light_manager.run()


async def connect_to_wifi():
    led = Led()
    flash_task = asyncio.create_task(led.flash())
    led_end = 1
    try:
        await wifi.connect()
    except Exception as exc:
        led_end = 0
        raise
    finally:
        flash_task.cancel()
        led.set(led_end)


if __name__ == "__main__":
    main()
