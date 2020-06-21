import asyncio

from dataset import MyDataset

class MyAsyncDataset:
    def __init__(self, path):
        self.ds = MyDataset(path)
        self.it = iter(self.ds)
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        try:
            data = next(self.it)
            await asyncio.sleep(data[0] * 1e-6)
            return data
        except StopIteration:
            raise StopAsyncIteration
        
async def iterate_through():
    async for data in MyAsyncDataset('/Users/ar_sabirov/2-Data/giant_test/my_dataset'):
        print(data[0])
        
        
def main():
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(iterate_through())
    finally:
        event_loop.close()


if __name__ == '__main__':
    main()