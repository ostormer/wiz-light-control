import asyncio
from pywizlight import wizlight, PilotBuilder, discovery
from time import sleep
from random import randint

BULB_IP = "192.168.0.198"


async def find_bulbs():
    """Sample code to work with bulbs."""
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list with wizlight objects.
    bulbs = await discovery.discover_lights(broadcast_space=BULB_IP)

    # Iterate over all returned bulbs
    for bulb in bulbs:
        print(bulb.__dict__)
        # Turn off all available bulbs
        # await bulb.turn_off()
    print(await bulbs[0].getBulbConfig())
    return bulbs


async def main_loop(bulbs):
    light = wizlight(bulbs[0].ip)
    magenta = (255, 0, 255)
    # Set bulb brightness (with async timeout)
    timeout = 10
    await asyncio.wait_for(light.turn_on(PilotBuilder(brightness=255)), timeout)
    await light.turn_on(PilotBuilder(rgb=magenta))
    for _ in range(50):
        await light.turn_on(PilotBuilder(rgb=magenta, brightness=randint(0, 100)))
        sleep(0.2)


loop = asyncio.get_event_loop()
light_bulbs = loop.run_until_complete(asyncio.gather(find_bulbs()))
loop.run_until_complete(main_loop(*light_bulbs))
