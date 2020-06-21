from pathlib import Path
from typing import List

import cv2
import numpy as np
import pandas as pd


def load_video(path: Path) -> List[np.ndarray]:
    cap = cv2.VideoCapture(str(path))

    frames = []
    ret = True
    while ret:
        ret, frame = cap.read()
        frames.append(frame)
    return frames


def load_image(path: Path) -> np.ndarray:
    return cv2.imread(str(path), 0)


def read_timestamps(path) -> pd.Series:
    return pd.read_csv(path, header=None)[0]


def read_touch(path) -> List[float]:
    with open(path, 'r') as fr:
        return [float(x) for x in fr.read().split(' ')]
