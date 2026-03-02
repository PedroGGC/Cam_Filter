import unittest
import numpy as np
import cv2
import sys
import os

# Ensure the root directory is in the path to import filters
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from filters import apply_pencil_sketch

class TestApplyPencilSketch(unittest.TestCase):
    def setUp(self):
        # Create a simple 10x10 BGR image
        self.frame = np.full((10, 10, 3), (100, 150, 200), dtype=np.uint8)

    def test_apply_pencil_sketch_output_shape_and_type(self):
        intensity = 0.5
        result = apply_pencil_sketch(self.frame, intensity)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.frame.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_apply_pencil_sketch_intensity_zero(self):
        # Even with intensity 0, a sketch should be created but with weight 0
        # Wait, the weight in the code is: weight = min(1.0, intensity * 1.5)
        # So weight = 0, meaning the original frame is returned fully!
        # return cv2.addWeighted(frame, 1.0 - weight, sketch_bgr, weight, 0)
        # So at intensity 0, result == frame
        intensity = 0.0
        result = apply_pencil_sketch(self.frame, intensity)
        np.testing.assert_array_equal(result, self.frame)

    def test_apply_pencil_sketch_divide_behavior(self):
        # The core operation of sketch is cv2.divide(gray, 255 - blur, scale=256)
        # We can test with a specific pattern to ensure divide doesn't crash
        # and produces expected results.
        # Let's create an image with pure black and pure white to test edge cases of divide.
        frame = np.zeros((10, 10, 3), dtype=np.uint8)
        frame[0:5, :] = 255  # Top half white
        frame[5:10, :] = 0   # Bottom half black

        intensity = 1.0
        result = apply_pencil_sketch(frame, intensity)

        # Ensure no crash, and result is valid
        self.assertEqual(result.shape, frame.shape)
        self.assertTrue(np.all(result >= 0) and np.all(result <= 255))

        # When intensity is 1.0, weight is min(1.0, 1.5) = 1.0
        # So it returns pure sketch.
        # Let's verify that the output isn't identical to input since it's blurred and divided
        # Actually, for pure white, gray is 255, inv is 0.
        # blur of 0 is 0. 255 - blur is 255.
        # divide(255, 255, scale=256) = 256 -> clipped to 255 (np.uint8).
        # So white should stay white.
        # For pure black, gray is 0, inv is 255.
        # blur of 255 is 255. 255 - blur is 0.
        # divide(0, 0, scale=256) -> in cv2.divide with 0 denominator, result is 0.
        # So black should stay black.
        # The boundary might have some variations due to blur.

        # Check pure white region (excluding boundary)
        np.testing.assert_array_equal(result[0:2, :], np.full((2, 10, 3), 255, dtype=np.uint8))

        # Check pure black region (excluding boundary)
        # Due to cv2.divide with 0 denominator, it should be 0.
        np.testing.assert_array_equal(result[8:10, :], np.zeros((2, 10, 3), dtype=np.uint8))

    def test_apply_pencil_sketch_random_noise(self):
        # A test to ensure we don't encounter divide by zero crashes or similar
        # issues on random noisy inputs.
        np.random.seed(42)
        frame = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        for intensity in [0.1, 0.5, 0.9]:
            result = apply_pencil_sketch(frame, intensity)
            self.assertEqual(result.shape, frame.shape)

if __name__ == '__main__':
    unittest.main()
