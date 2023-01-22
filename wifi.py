import network
import uasyncio as asyncio


WIFI_SSID = ""
WIFI_PASSWORD = ""


async def connect():
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
        await asyncio.sleep(1)
        
    raise Exception("TIMEOUT")
