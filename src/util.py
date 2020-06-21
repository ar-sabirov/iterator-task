from pathlib import Path

import cv2
import pandas as pd


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
