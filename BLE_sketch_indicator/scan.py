import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print ("----------------------------------")
        print(d)
        print(d.address)
        print(d.details)
        print(d.metadata)

asyncio.run(main())
