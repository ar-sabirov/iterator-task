import asyncio

from .dataset import MyDataset


class MyAsyncDataset:
    def __init__(self, path, unit_conversion: float):
        self.ds = MyDataset(path)
        self.unit_conversion = unit_conversion
        self.it = None
        self.prev_ts = 0

    def __aiter__(self):
        self.it = iter(self.ds)
        return self

    async def __anext__(self):
        try:
            data = next(self.it)
            delay = (data['touch_ts'] - self.prev_ts) * self.unit_conversion
            self.prev_ts = data['touch_ts']
            await asyncio.sleep(delay=delay)
            return data
        except StopIteration:
            raise StopAsyncIteration
