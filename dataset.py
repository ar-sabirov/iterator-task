from pathlib import Path

import pandas as pd

from util import (get_indicies, load_image, load_video, read_timestamps,
                  read_touch)


class MyDataset:
    def __init__(self, path: str):
        self.root_path = Path(path)
        self.rgb_path = self.root_path / 'rgb'
        self.depth_path = self.root_path / 'depth'
        self.touch_path = self.root_path / 'touch'

    def __iter__(self):
        self.depth_files = sorted(self.depth_path.glob('frame-*.png'))
        self.touch_files = sorted(self.touch_path.glob('observation-*.txt'))
        self.rgb_frames = load_video(self.rgb_path / 'video.mp4')

        rgb_ts = read_timestamps(self.rgb_path / 'per_frame_timestamps.txt')
        depth_ts = read_timestamps(
            self.depth_path / 'per_frame_timestamps.txt')
        self.touch_ts = read_timestamps(
            self.touch_path / 'per_observation_timestamps.txt')

        self.indicies = get_indicies(rgb_ts, depth_ts, self.touch_ts)

        self._i = 0
        self._limit = len(self.indicies)

        return self

    def __next__(self):
        if self._i == self._limit:
            raise StopIteration

        ind = self.indicies[self._i]
        touch_idx, rgb_idx, depth_idx = ind['touch'], ind['rgb'], ind['depth']

        touch_timestamp_i = self.touch_ts[touch_idx]
        print('-'*10)
        print(f'{self._i}')
        print(f'Touch: {self.touch_files[touch_idx]}')
        print(f'Depth: {self.depth_files[depth_idx]}')
        print(f'rgb idx: {rgb_idx}')
        touch_i = read_touch(self.touch_files[touch_idx])
        rgb_j = self.rgb_frames[rgb_idx]
        depth_k = load_image(self.depth_files[depth_idx])

        self._i += 1

        return touch_timestamp_i, touch_i, rgb_j, depth_k


if __name__ == "__main__":
    ds = MyDataset('/Users/ar_sabirov/2-Data/giant_test/my_dataset')
    for touch_timestamp_i, touch_i, rgb_j, depth_k in ds:
        pass
