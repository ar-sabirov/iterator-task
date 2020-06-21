from pathlib import Path

import pandas as pd

from .indicies import get_indicies
from .util import load_image, load_video, read_timestamps, read_touch
from logging import getLogger

logger = getLogger(__name__)

class MyDataset:
    def __init__(self,
                 path: str,
                 unit='us'):
        self.root_path = Path(path)
        self.rgb_path = self.root_path / 'rgb'
        self.depth_path = self.root_path / 'depth'
        self.touch_path = self.root_path / 'touch'
        self.unit = unit

    def __iter__(self):
        self.depth_files = sorted(self.depth_path.glob('frame-*.png'))
        self.touch_files = sorted(self.touch_path.glob('observation-*.txt'))
        
        logger.debug('Depth files:\n%s', self.depth_files)
        logger.debug('Touch files:\n%s', self.touch_files)
        
        self.rgb_frames = load_video(self.rgb_path / 'video.mp4')
        
        logger.debug('Num of video frames: %s', len(self.rgb_frames))
        rgb_ts = read_timestamps(self.rgb_path / 'per_frame_timestamps.txt')
        depth_ts = read_timestamps(self.depth_path / 'per_frame_timestamps.txt')
        self.touch_ts = read_timestamps(
            self.touch_path / 'per_observation_timestamps.txt')

        self.indicies = get_indicies(rgb_ts,
                                     depth_ts,
                                     self.touch_ts,
                                     unit=self.unit)

        self._i = 0
        self._limit = len(self.indicies)

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
