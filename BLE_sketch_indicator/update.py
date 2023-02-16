from bleak import BleakClient
from config import config


async def update_sketch_queue_indicator(left, right):

    address = config["SKETCH_QUEUE_BLE_ADDRESS"]

    print("attempting to connect")
    async with BleakClient(address) as client:
        # find chars
        # chars = client.services.characteristics
        # print(chars)
        # return

        initial = await client.read_gatt_char(10)
        print("initial:", initial)

        out = await client.write_gatt_char(10, bytearray([left]), True)
        out = await client.write_gatt_char(12, bytearray([right]), True)
        print(out)