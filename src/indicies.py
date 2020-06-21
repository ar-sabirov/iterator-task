from functools import reduce
from typing import Dict, List

import pandas as pd


def get_indicies(rgb_arr: List[int],
                 depth_arr: List[int],
                 touch_arr: List[int],
                 unit: str = 'us') -> List[Dict[str, int]]:
    """Computes indicies depth and rgb timestamps that are closest
    to touch timestamps

    Example: tests/test_indicies.py

    Parameters
    ----------
    rgb_arr : List[int]
        Video timestamps
    depth_arr : List[int]
        Depth timestamps
    touch_arr : List[int]
        Touch timestamps
    unit : str, optional
        Unit to use in pd.to_timedelta
        (e.g 'ms', 'us', 'ns'), by default 'us'

    Returns
    -------
    List[Dict[str, int]]
        List dicts with indicies
        Sample result: 
            [{'depth': 0, 'rgb': 0, 'touch': 0},
                ...
            {'depth': 15, 'rgb': 22, 'touch': 6}]
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

    return df.reset_index(drop=True).to_dict(orient='records')
