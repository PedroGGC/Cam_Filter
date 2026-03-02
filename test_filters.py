import unittest
import numpy as np
import cv2
from filters import apply_blueprint

class TestApplyBlueprint(unittest.TestCase):
    def setUp(self):
        # Create a simple 100x100 BGR frame for tests
        self.frame = np.zeros((100, 100, 3), dtype=np.uint8)

    def test_output_shape_and_type(self):
        """Test that the output has the same shape and type as the input."""
        res = apply_blueprint(self.frame, 0.5)
        self.assertEqual(res.shape, self.frame.shape)
        self.assertEqual(res.dtype, np.uint8)

    def test_background_color_low_intensity(self):
        """Test that low intensity (<0.1) produces solid background without grid when there are no edges."""
        # When intensity is 0.0, apply_blueprint should not add the grid
        res = apply_blueprint(self.frame, 0.0)

        # Check that all pixels are the background color (150, 50, 20)
        unique_pixels = np.unique(res.reshape(-1, 3), axis=0)
        self.assertEqual(len(unique_pixels), 1)
        self.assertTrue(np.array_equal(unique_pixels[0], [150, 50, 20]))

    def test_grid_lines_high_intensity(self):
        """Test that high intensity (>0.1) applies grid lines with color (180, 80, 40)."""
        intensity = 0.5
        res = apply_blueprint(self.frame, intensity)

        # Expected grid size when intensity is 0.5
        grid_size = max(15, int(70 - intensity * 50))

        # Check that the first row/col has the grid color
        self.assertTrue(np.array_equal(res[0, 0], [180, 80, 40]))
        self.assertTrue(np.array_equal(res[grid_size, grid_size], [180, 80, 40]))

        # Check a pixel that is not on the grid (assuming grid_size > 1 and it doesn't fall on grid)
        self.assertTrue(np.array_equal(res[1, 1], [150, 50, 20]))

    def test_edge_detection(self):
        """Test that an image with a sharp edge produces bright lines representing the edge."""
        # Create an image with a clear vertical edge
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, 50:] = 255

        res = apply_blueprint(frame, 0.0)

        # Check that there are bright pixels indicating an edge
        self.assertTrue(np.any(res == 255))

        # Verify that the edge is detected around the middle
        edge_region = res[:, 45:55]
        self.assertTrue(np.any(edge_region == 255))

if __name__ == '__main__':
    unittest.main()
