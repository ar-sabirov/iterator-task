import asyncio

from .dataset import MyDataset


class MyAsyncDataset:
    def __init__(self, path, unit_conversion: float = 1e-3):
        self.ds = MyDataset(path)
        self.unit_conversion = unit_conversion
        self.it = None

    def __aiter__(self):
        self.it = iter(self.ds)
        return self

    async def __anext__(self):
        try:
            data = next(self.it)
            await asyncio.sleep(data[0] * self.unit_conversion)
            return data
        except StopIteration:
            raise StopAsyncIteration
