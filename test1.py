import pyrcrack

from rich.console import Console
from rich.prompt import Prompt
import asyncio


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    airmon = pyrcrack.AirmonNg()

    #interface = Prompt.ask(
    #    'Select an interfaceV',
    #    choices=[a['interface'] for a in await airmon.interfaces])

    async with airmon("wlan1") as mon:
        async with pyrcrack.AirodumpNg() as pdump:
            async for result in pdump(mon.monitor_interface):
                console.clear()
                console.print(result.table)
                await asyncio.sleep(2)


asyncio.run(scan_for_targets())
