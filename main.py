import network, utime
import uasyncio as asyncio

from handler import EasyMorningHandler
from lightmanager import LightManager

WIFI_SSID = ""
WIFI_PASSWORD = ""


def main():
    try:
        connect_to_wifi()
    except Exception as exc:
        print("could not connect to wifi:", exc)
        
    asyncio.run(async_main())


async def async_main():
    light_manager = LightManager()
    handler = EasyMorningHandler(light_manager)
    asyncio.create_task(asyncio.start_server(handler.handle_connection, "0.0.0.0", 80))
    await light_manager.run()


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # turn off power saving mode off
    wlan.config(pm = 0xa11140)
    wlan.connect(
        ssid=WIFI_SSID,
        key=WIFI_PASSWORD,
    )

    for i in range(10):
        if wlan.isconnected():
            ip, subnet, gateway, dns = wlan.ifconfig()
            print("connect to wifi")
            print("ip:", ip)
            return
        elif wlan.status() == network.STAT_WRONG_PASSWORD:
            raise Exception("WRONG_PASSWORD")
        elif wlan.status() == network.STAT_NO_AP_FOUND:
            raise Exception("NO_AP_FOUND")
        elif wlan.status() == network.STAT_CONNECT_FAIL:
            raise Exception("CONNECT_FAIL")
        utime.sleep(1)
        
    raise Exception("TIMEOUT")
    

if __name__ == "__main__":
    main()
