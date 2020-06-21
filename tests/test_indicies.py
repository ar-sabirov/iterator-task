import sys
import unittest
from os import linesep
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).absolute().parent.parent))
from src.indicies import get_indicies

class TestIndicies(unittest.TestCase):

    def test_get_indicies(self):
        """Tests if indicies are correctly generated
        on sample synthetic data
        """
        rgb_arr = np.arange(0, 200, 9)
        depth_arr = np.arange(0, 250, 16)
        touch_arr = np.arange(0, 350, 50)

        expected = pd.DataFrame(
            {'depth': [0, 48, 96,  144, 208, 240, 240],
             'rgb':   [0, 54, 99,  153, 198, 198, 198],
             'touch': [0, 50, 100, 150, 200, 250, 300]})

        indicies = pd.DataFrame(get_indicies(rgb_arr, depth_arr, touch_arr))
        actual = pd.DataFrame({'depth': depth_arr[indicies['depth']],
                               'rgb': rgb_arr[indicies['rgb']],
                               'touch': touch_arr[indicies['touch']]})

        print(f'Expected:{linesep}{expected}')
        print(f'Actual:{linesep}{actual}')

        pd.testing.assert_frame_equal(expected, actual)


if __name__ == "__main__":
    unittest.main()
