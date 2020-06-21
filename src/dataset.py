from logging import getLogger
from os import linesep
from pathlib import Path

from .indicies import get_indicies
from .util import load_image, load_video, read_timestamps, read_touch

logger = getLogger(__name__)


class MyDataset:
    def __init__(self,
                 path: str,
                 unit='us'):
        root_path = Path(path)
        rgb_path = root_path / 'rgb'
        depth_path = root_path / 'depth'
        touch_path = root_path / 'touch'

        self.depth_files = sorted(depth_path.glob('frame-*.png'))
        self.touch_files = sorted(touch_path.glob('observation-*.txt'))

        logger.debug(f'Depth files: {linesep} {self.depth_files}')
        logger.debug(f'Touch files: {linesep} {self.touch_files}')

        rgb_frames = load_video(rgb_path / 'video.mp4')
        logger.debug(f'Num of video frames: {len(rgb_frames)}')

        rgb_ts = read_timestamps(rgb_path / 'per_frame_timestamps.txt')
        depth_ts = read_timestamps(depth_path / 'per_frame_timestamps.txt')
        touch_ts = read_timestamps(
            touch_path / 'per_observation_timestamps.txt')

        self.indicies = get_indicies(rgb_ts,
                                     depth_ts,
                                     touch_ts,
                                     unit=unit)
        self.rgb_frames = rgb_frames
        self.touch_ts = touch_ts
        self._i = None
        self._limit = len(self.indicies)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i == self._limit:
            raise StopIteration

        ind = self.indicies[self._i]
        touch_idx, rgb_idx, depth_idx = ind['touch'], ind['rgb'], ind['depth']

        logger.debug(f'{self._i}')
        logger.debug(f'Touch: {self.touch_files[touch_idx]}')
        logger.debug(f'Depth: {self.depth_files[depth_idx]}')
        logger.debug(f'rgb idx: {rgb_idx}')

        touch_timestamp_i = self.touch_ts[touch_idx]
        touch_i = read_touch(self.touch_files[touch_idx])
        rgb_j = self.rgb_frames[rgb_idx]
        depth_k = load_image(self.depth_files[depth_idx])

        self._i += 1

        return touch_timestamp_i, touch_i, rgb_j, depth_k
