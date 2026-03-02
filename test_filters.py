import unittest
import numpy as np
import cv2
from filters import (
    apply_deep_dive, apply_gameboy, apply_blueprint, apply_crt,
    apply_neon_edges, apply_pixelate, apply_glitch, apply_pencil_sketch,
    apply_halftone, apply_ghost_trails, apply_ascii_contrast, Filter
)

class TestFilters(unittest.TestCase):
    def setUp(self):
        # Create a standard 100x100 BGR dummy frame
        self.dummy_frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        # Create a 100x100 grayscale dummy frame for grayscale specific filters
        self.dummy_gray = np.random.randint(0, 256, (100, 100), dtype=np.uint8)

    def test_apply_deep_dive(self):
        result = apply_deep_dive(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Test edge case: intensity 0 and 1
        res0 = apply_deep_dive(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)
        res1 = apply_deep_dive(self.dummy_frame, intensity=1.0)
        self.assertEqual(res1.shape, self.dummy_frame.shape)

    def test_apply_gameboy(self):
        result = apply_gameboy(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Test edge case: intensity 0
        res0 = apply_gameboy(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)

    def test_apply_blueprint(self):
        result = apply_blueprint(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Intensity < 0.1 case
        res0 = apply_blueprint(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)

    def test_apply_crt(self):
        result = apply_crt(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Intensity <= 0 case
        res0 = apply_crt(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)

    def test_apply_neon_edges(self):
        result = apply_neon_edges(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Test edge case: intensity 0
        res0 = apply_neon_edges(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)

    def test_apply_pixelate(self):
        result = apply_pixelate(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Intensity low enough to trigger block == 1
        res0 = apply_pixelate(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)

    def test_apply_glitch(self):
        result = apply_glitch(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Shift <= 0 case
        res0 = apply_glitch(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)

    def test_apply_pencil_sketch(self):
        result = apply_pencil_sketch(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Extreme intensities
        res0 = apply_pencil_sketch(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)
        res1 = apply_pencil_sketch(self.dummy_frame, intensity=1.0)
        self.assertEqual(res1.shape, self.dummy_frame.shape)

    def test_apply_halftone(self):
        result = apply_halftone(self.dummy_frame, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_frame.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Test extreme intensities
        res0 = apply_halftone(self.dummy_frame, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_frame.shape)
        res1 = apply_halftone(self.dummy_frame, intensity=1.0)
        self.assertEqual(res1.shape, self.dummy_frame.shape)

    def test_apply_ghost_trails(self):
        # Reset the attribute if it exists from other tests running
        if hasattr(apply_ghost_trails, "last_frame"):
            delattr(apply_ghost_trails, "last_frame")

        result1 = apply_ghost_trails(self.dummy_frame, intensity=0.5)
        self.assertEqual(result1.shape, self.dummy_frame.shape)
        self.assertEqual(result1.dtype, np.uint8)

        # Apply again to test the path where last_frame exists
        result2 = apply_ghost_trails(self.dummy_frame, intensity=0.5)
        self.assertEqual(result2.shape, self.dummy_frame.shape)
        self.assertEqual(result2.dtype, np.uint8)

    def test_apply_ascii_contrast(self):
        # Note: this filter expects a grayscale frame
        result = apply_ascii_contrast(self.dummy_gray, intensity=0.5)
        self.assertEqual(result.shape, self.dummy_gray.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Test extreme intensities
        res0 = apply_ascii_contrast(self.dummy_gray, intensity=0.0)
        self.assertEqual(res0.shape, self.dummy_gray.shape)
        res1 = apply_ascii_contrast(self.dummy_gray, intensity=1.0)
        self.assertEqual(res1.shape, self.dummy_gray.shape)


if __name__ == '__main__':
    unittest.main()
