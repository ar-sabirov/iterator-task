import asyncio
import logging
from logging.config import fileConfig

import click

fileConfig('logging_config.ini')
logger = logging.getLogger()

from src.async_dataset import MyAsyncDataset
from src.dataset import MyDataset


@click.command()
@click.option('--path', '-p', type=str, help='Path to dataset folder')
@click.option('--delayed', '-d', type=bool, default=False, help='Use delays')
def main(**params):
    path = params['path']
    if params['delayed']:
        delayed_run(path)
    else:
        run(path)


def delayed_run(path):
    async def delayed_iterate(ds):
        async for data in ds:
            logger.info(data[0])

    ds = MyAsyncDataset(path, unit_conversion=1e-2)
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(delayed_iterate(ds))
    finally:
        event_loop.close()


def run(path):
    ds = MyDataset(path)
    for data in ds:
        logger.info(data[0])


if __name__ == "__main__":
    main()
