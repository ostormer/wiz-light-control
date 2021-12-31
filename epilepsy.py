import asyncio
from pywizlight import wizlight, PilotBuilder, discovery
from time import sleep
from random import randint, choice
from tqdm import tqdm

BULB_IP = "192.168.0.198"

COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "pink": (255, 0, 255),
    "cyan": (0, 191, 255),
    "orange": (255, 63, 0),
    
}

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

        color = choice(list(COLORS.keys()))
        print(color)
        await light.turn_on(PilotBuilder(
            rgb=COLORS[color]
            ))
        sleep(2)
        await light.turn_off()
        


loop = asyncio.get_event_loop()
light_bulbs = loop.run_until_complete(asyncio.gather(find_bulbs()))
loop.run_until_complete(main_loop(*light_bulbs))
