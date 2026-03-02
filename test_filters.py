import unittest
import numpy as np
import cv2
from filters import apply_halftone

class TestFilters(unittest.TestCase):
    def test_apply_halftone_basic(self):
        # Create a random RGB image (h=100, w=150, c=3)
        frame = np.random.randint(0, 256, (100, 150, 3), dtype=np.uint8)
        intensity = 0.5

        result = apply_halftone(frame, intensity)

        self.assertEqual(result.shape, frame.shape, "Output shape should match input shape")
        self.assertEqual(result.dtype, np.uint8, "Output dtype should be uint8")

    def test_apply_halftone_output_values(self):
        # Create a varied image
        frame = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        result = apply_halftone(frame, 0.5)

        # Output values should only be (230, 230, 230) or (10, 10, 10)
        unique_colors = np.unique(result.reshape(-1, 3), axis=0)
        for color in unique_colors:
            is_valid = np.array_equal(color, [230, 230, 230]) or np.array_equal(color, [10, 10, 10])
            self.assertTrue(is_valid, f"Unexpected color found in halftone output: {color}")

    def test_apply_halftone_grid_placement_black(self):
        # Test with a black image: circles should be maximum size
        intensity = 0.5
        block_size = max(4, int(intensity * 24)) # 12
        h, w = 60, 60
        frame = np.zeros((h, w, 3), dtype=np.uint8)

        result = apply_halftone(frame, intensity)

        # Check centers
        for y in range(h):
            for x in range(w):
                if y % block_size == block_size // 2 and x % block_size == block_size // 2:
                    # dist_sq = 0 <= radii_sq, so it should be dark
                    self.assertTrue(np.array_equal(result[y, x], [10, 10, 10]))
                if y % block_size == 0 and x % block_size == 0:
                    # dist_sq = 2 * (block_size // 2)^2 > radii_sq = (block_size // 2)^2
                    self.assertTrue(np.array_equal(result[y, x], [230, 230, 230]))

    def test_apply_halftone_grid_placement_white(self):
        # Test with a white image: circles should be minimum size (only center pixel)
        intensity = 0.5
        block_size = max(4, int(intensity * 24)) # 12
        h, w = 60, 60
        frame = np.full((h, w, 3), 255, dtype=np.uint8)

        result = apply_halftone(frame, intensity)

        # Count number of dark pixels, should be exactly 1 per block
        dark_pixels = np.sum(np.all(result == [10, 10, 10], axis=-1))
        expected_dark_pixels = (h // block_size) * (w // block_size)
        self.assertEqual(dark_pixels, expected_dark_pixels)

        # Verify they are exactly at the centers
        for y in range(h):
            for x in range(w):
                if y % block_size == block_size // 2 and x % block_size == block_size // 2:
                    self.assertTrue(np.array_equal(result[y, x], [10, 10, 10]))
                else:
                    self.assertTrue(np.array_equal(result[y, x], [230, 230, 230]))

if __name__ == '__main__':
    unittest.main()
