import unittest
import numpy as np
import cv2
from filters import apply_gameboy

class TestFilters(unittest.TestCase):
    def setUp(self):
        # The expected gameboy palette
        self.palette_bgr = np.array([
            [15, 56, 15],
            [48, 98, 48],
            [15, 172, 139],
            [15, 188, 155],
        ], dtype=np.uint8)

    def test_apply_gameboy_shape(self):
        # Output should have same shape as input
        frame = np.random.randint(0, 256, (100, 150, 3), dtype=np.uint8)

        res = apply_gameboy(frame, 0.5)
        self.assertEqual(res.shape, frame.shape)

        res_zero = apply_gameboy(frame, 0.0)
        self.assertEqual(res_zero.shape, frame.shape)

        res_one = apply_gameboy(frame, 1.0)
        self.assertEqual(res_one.shape, frame.shape)

    def test_apply_gameboy_colors_in_palette(self):
        # All colors in the output must belong to the palette
        frame = np.random.randint(0, 256, (80, 80, 3), dtype=np.uint8)

        # Test a few intensities
        for intensity in [0.0, 0.2, 0.5, 0.8, 1.0]:
            res = apply_gameboy(frame, intensity)

            # Reshape to a list of pixels
            reshaped_res = res.reshape(-1, 3)

            # Check if each pixel is in the palette
            matches = np.all(reshaped_res[:, None, :] == self.palette_bgr[None, :, :], axis=2)
            valid_pixels = np.any(matches, axis=1)

            self.assertTrue(np.all(valid_pixels), f"Found colors outside palette at intensity {intensity}")

    def test_apply_gameboy_solid_colors(self):
        # Solid black should map to the darkest palette color
        black_frame = np.zeros((50, 50, 3), dtype=np.uint8)
        res_black = apply_gameboy(black_frame, 0.5)
        expected_darkest = self.palette_bgr[0] # [15, 56, 15]
        self.assertTrue(np.all(res_black == expected_darkest))

        # Solid white should map to the lightest palette color
        white_frame = np.full((50, 50, 3), 255, dtype=np.uint8)
        res_white = apply_gameboy(white_frame, 0.5)
        expected_lightest = self.palette_bgr[3] # [15, 188, 155]
        self.assertTrue(np.all(res_white == expected_lightest))

    def test_apply_gameboy_intensity_effect(self):
        # High intensity should result in larger blocks (lower effective resolution)
        frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

        res_low = apply_gameboy(frame, 0.0)
        res_high = apply_gameboy(frame, 1.0)

        # High intensity means block > 1, so the result should have repeating blocks
        # For intensity 1.0, block = int(1.0 * 15) + 1 = 16
        # The result will be blocky, meaning neighboring pixels will often be identical
        # We can test this by checking the number of unique rows/cols or just ensuring
        # it differs from the low intensity output for a random noise image.
        self.assertFalse(np.array_equal(res_low, res_high))

if __name__ == '__main__':
    unittest.main()
