import unittest
import numpy as np
import filters

class TestFilters(unittest.TestCase):

    def setUp(self):
        # Create a dummy frame (height, width, channels)
        # We'll use a 10x10x3 image frame filled with increasing numbers to make shifts detectable
        self.frame = np.arange(300, dtype=np.uint8).reshape((10, 10, 3))

    def test_apply_glitch_zero_intensity(self):
        """Test apply_glitch with 0 intensity returns the exact original frame."""
        intensity = 0.0
        result = filters.apply_glitch(self.frame, intensity)

        # Verify it returns the exact same object
        self.assertIs(result, self.frame)
        # Verify the contents are identical
        np.testing.assert_array_equal(result, self.frame)

    def test_apply_glitch_negative_intensity(self):
        """Test apply_glitch with negative intensity returns the exact original frame."""
        intensity = -0.5
        result = filters.apply_glitch(self.frame, intensity)

        # Verify it returns the exact same object
        self.assertIs(result, self.frame)
        # Verify the contents are identical
        np.testing.assert_array_equal(result, self.frame)

    def test_apply_glitch_positive_intensity(self):
        """Test apply_glitch with positive intensity modifies the frame correctly."""
        intensity = 0.05  # shift = 5
        result = filters.apply_glitch(self.frame, intensity)

        # Verify it returns a new object
        self.assertIsNot(result, self.frame)

        # Verify the red channel (index 0) is shifted by -5
        expected_r = np.roll(self.frame[:, :, 0], -5, axis=1)
        np.testing.assert_array_equal(result[:, :, 0], expected_r)

        # Verify the green channel (index 1) is unchanged
        np.testing.assert_array_equal(result[:, :, 1], self.frame[:, :, 1])

        # Verify the blue channel (index 2) is shifted by +5
        expected_b = np.roll(self.frame[:, :, 2], 5, axis=1)
        np.testing.assert_array_equal(result[:, :, 2], expected_b)

if __name__ == '__main__':
    unittest.main()
