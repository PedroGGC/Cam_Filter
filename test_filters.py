import unittest
import numpy as np
from filters import apply_deep_dive

class TestFilters(unittest.TestCase):
    def test_apply_deep_dive_basic(self):
        """Test basic functionality with a simple frame."""
        frame = np.array([[[100, 150, 200]]], dtype=np.uint8)

        # Test with intensity 0 (max levels: 32)
        # levels = 32, ratio = 256.0 / 32 = 8.0
        # quantized = np.floor(frame / 8.0) * 8.0
        # expected: floor([100, 150, 200] / 8) * 8 = [12, 18, 25] * 8 = [96, 144, 200]
        res0 = apply_deep_dive(frame, 0.0)
        np.testing.assert_array_equal(res0, np.array([[[96, 144, 200]]], dtype=np.uint8))

        # Test with intensity 1.0 (min levels: 2)
        # levels = max(2, int(32 - 30)) = 2
        # ratio = 256.0 / 2 = 128.0
        # quantized = np.floor([100, 150, 200] / 128) * 128 = [0, 1, 1] * 128 = [0, 128, 128]
        res1 = apply_deep_dive(frame, 1.0)
        np.testing.assert_array_equal(res1, np.array([[[0, 128, 128]]], dtype=np.uint8))

        # Test with intensity 0.5 (levels: 17)
        # levels = max(2, int(32 - 15)) = 17
        # ratio = 256.0 / 17 = 15.0588...
        # quantized = np.floor([100, 150, 200] / 15.0588) * 15.0588
        # [100, 150, 200] / 15.0588 = [6.64, 9.96, 13.28] -> floor -> [6, 9, 13]
        # [6, 9, 13] * 15.0588 = [90.35, 135.53, 195.76] -> uint8 -> [90, 135, 195]
        res_half = apply_deep_dive(frame, 0.5)
        np.testing.assert_array_equal(res_half, np.array([[[90, 135, 195]]], dtype=np.uint8))

    def test_apply_deep_dive_edge_cases(self):
        """Test with 0, 255 values."""
        frame = np.array([[[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)

        res0 = apply_deep_dive(frame, 0.0)
        # 0 / 8 = 0 -> 0
        # 255 / 8 = 31.875 -> 31 * 8 = 248
        np.testing.assert_array_equal(res0, np.array([[[0, 0, 0], [248, 248, 248]]], dtype=np.uint8))

        res1 = apply_deep_dive(frame, 1.0)
        # 0 / 128 = 0 -> 0
        # 255 / 128 = 1.99 -> 1 * 128 = 128
        np.testing.assert_array_equal(res1, np.array([[[0, 0, 0], [128, 128, 128]]], dtype=np.uint8))

    def test_apply_deep_dive_shapes(self):
        """Ensure the output shape matches input and is of type uint8."""
        frame = np.zeros((10, 20, 3), dtype=np.uint8)
        res = apply_deep_dive(frame, 0.5)
        self.assertEqual(res.shape, (10, 20, 3))
        self.assertEqual(res.dtype, np.uint8)

    def test_apply_deep_dive_negative_intensity(self):
        """Test with negative intensity to ensure it doesn't crash."""
        frame = np.array([[[100, 150, 200]]], dtype=np.uint8)
        # levels = max(2, int(32 - (-1.0 * 30))) = max(2, 62) = 62
        # ratio = 256.0 / 62 = 4.129
        # 100 / 4.129 = 24.2 -> 24 * 4.129 = 99.09 -> 99
        res_neg = apply_deep_dive(frame, -1.0)
        self.assertEqual(res_neg.dtype, np.uint8)
        self.assertEqual(res_neg.shape, frame.shape)

    def test_apply_deep_dive_high_intensity(self):
        """Test with intensity > 1.0."""
        frame = np.array([[[100, 150, 200]]], dtype=np.uint8)
        # intensity 2.0 -> int(32 - 60) = -28
        # levels = max(2, -28) = 2
        res_high = apply_deep_dive(frame, 2.0)
        np.testing.assert_array_equal(res_high, np.array([[[0, 128, 128]]], dtype=np.uint8))

if __name__ == '__main__':
    unittest.main()
