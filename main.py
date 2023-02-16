import asyncio
from BLE_sketch_indicator.update import update_sketch_queue_indicator
import cloudprint_api.api as api

# run it
if __name__ == "__main__":
    kyle, caroline = api.get_queue_count()
    asyncio.run(update_sketch_queue_indicator(kyle, caroline))