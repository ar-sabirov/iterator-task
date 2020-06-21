from functools import reduce
from pathlib import Path
from typing import List

import cv2
import pandas as pd


def get_indicies(rgb_arr: List[int],
                 depth_arr: List[int],
                 touch_arr: List[int],
                 unit: str = 'us') -> List[List[int]]:
    """
                            touch  depth  rgb
        00:00:00             0      0    0
        00:00:00.000050      1      3    6
        00:00:00.000100      2      6   11
        00:00:00.000150      3      9   17
        00:00:00.000200      4     13   17
        00:00:00.000250      5     13   17
        00:00:00.000300      6     13   17
    """
    sr_rgb = pd.Series(rgb_arr)
    sr_depth = pd.Series(depth_arr)
    sr_touch = pd.Series(touch_arr)

    touch_ts = pd.Series(index=pd.to_timedelta(sr_touch, unit=unit),
                         data=sr_touch.index,
                         name='touch')

    depth_ts = pd.Series(index=pd.to_timedelta(sr_depth, unit=unit),
                         data=sr_depth.index,
                         name='depth').reindex(touch_ts.index, method='nearest')

    rgb_ts = pd.Series(index=pd.to_timedelta(sr_rgb, unit=unit),
                       data=sr_rgb.index,
                       name='rgb').reindex(touch_ts.index, method='nearest')

    to_merge = [touch_ts, depth_ts, rgb_ts]

    df = reduce(
        lambda a, b: pd.merge(a, b, right_index=True,
                              left_index=True, how='outer'),
        to_merge)

    df = df.fillna(method='ffill').astype(int)
    df = df.iloc[0:len(sr_touch)]

    with pd.option_context('display.max_rows', 100):
        test_df = pd.DataFrame({'touch': sr_touch,
                                'depth': sr_depth[depth_ts].reset_index(drop=True),
                                'rgb': sr_rgb[rgb_ts].reset_index(drop=True)})
        print('Alligned timestamps')
        print(test_df)
        print('Alligned indicies')
        print(df)

    return df.reset_index(drop=True).to_dict(orient='records')


def load_video(path: Path):
    cap = cv2.VideoCapture(str(path))

    frames = []
    ret = True
    while ret:
        ret, frame = cap.read()
        frames.append(frame)
    return frames


def load_image(path: Path):
    return cv2.imread(str(path), 0)


def read_timestamps(path):
    return pd.read_csv(path, header=None)[0]


def read_touch(path):
    with open(path, 'r') as fr:
        return [float(x) for x in fr.read().split(' ')]


def main():
    import numpy as np
    rgb_arr = np.arange(0, 200, 9)
    depth_arr = np.arange(0, 250, 16)
    touch_arr = np.arange(0, 350, 50)
    get_indicies(rgb_arr, depth_arr, touch_arr)


if __name__ == "__main__":
    main()
