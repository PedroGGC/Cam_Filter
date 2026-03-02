import unittest
import numpy as np
import cv2
from filters import apply_pixelate

class TestFilters(unittest.TestCase):
    def test_apply_pixelate_edge_case(self):
        frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

        # When intensity is very low (e.g., 0.01), block == 1 should be True
        # block = max(1, int(intensity * 100))
        # int(0.01 * 100) = 1, so block = 1
        intensity = 0.01

        result = apply_pixelate(frame, intensity)

        # Since block == 1, the function should return the original frame unmodified
        # We can test this by checking if they share the same memory (identity) or are equal
        np.testing.assert_array_equal(result, frame)
        self.assertIs(result, frame, "The returned frame should be the exact same object when block == 1")

if __name__ == '__main__':
    unittest.main()
