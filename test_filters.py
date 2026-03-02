import unittest
import numpy as np
import cv2
from filters import apply_neon_edges

class TestFilters(unittest.TestCase):

    def test_apply_neon_edges_high_contrast(self):
        # Create a 100x100 black image with a white square in the middle to ensure strong edges
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[25:75, 25:75] = [255, 255, 255]

        result = apply_neon_edges(frame, 1.0)

        # Verify output shape matches input
        self.assertEqual(result.shape, frame.shape)
        # Verify dtype is np.uint8
        self.assertEqual(result.dtype, np.uint8)

        # Check that there are non-zero pixels (edges detected and glow applied)
        self.assertTrue(np.any(result > 0))

        # The center of the square should remain dark because there are no edges
        self.assertTrue(np.all(result[50, 50] == 0))

        # Check for neon green color characteristic (green channel high due to [0, 255, 65] BGR)
        # The max green value should be high due to the strong neon edge application
        self.assertTrue(np.max(result[:, :, 1]) > 100)

    def test_apply_neon_edges_zero_intensity(self):
        # Create a uniform gray image
        frame = np.full((100, 100, 3), 128, dtype=np.uint8)

        result = apply_neon_edges(frame, 0.0)

        # Since intensity is 0.0, dark = frame * 1.0.
        # result = dark + edges_with_glow * 0 = frame
        self.assertTrue(np.array_equal(result, frame))

    def test_apply_neon_edges_blank_image(self):
        # Create a completely black image
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        result = apply_neon_edges(frame, 1.0)

        # No edges in a completely black image, result should be the same as input
        self.assertTrue(np.array_equal(result, frame))

if __name__ == '__main__':
    unittest.main()
