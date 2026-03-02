import unittest
import numpy as np
import cv2
from filters import apply_blueprint

class TestApplyBlueprint(unittest.TestCase):
    def test_apply_blueprint_basic(self):
        # Create a basic 100x100 white image
        frame = np.full((100, 100, 3), 255, dtype=np.uint8)

        # Apply blueprint with intensity 0 (no grid)
        result = apply_blueprint(frame, 0.0)

        # Check shape is maintained
        self.assertEqual(result.shape, (100, 100, 3))

        # Since it's a solid white image, there are no edges
        # The background color is (150, 50, 20) in BGR
        expected_bg = np.array([150, 50, 20], dtype=np.uint8)
        self.assertTrue(np.all(result[0, 0] == expected_bg))

        # Ensure the whole image is expected_bg (since grid is not drawn)
        self.assertTrue(np.all(result == expected_bg))

    def test_apply_blueprint_with_grid(self):
        # Create a basic 100x100 white image
        frame = np.full((100, 100, 3), 255, dtype=np.uint8)

        # Apply blueprint with high intensity (>0.1 triggers grid)
        intensity = 0.5
        result = apply_blueprint(frame, intensity)

        # Check shape is maintained
        self.assertEqual(result.shape, (100, 100, 3))

        # Grid color should be present: (180, 80, 40)
        grid_color = np.array([180, 80, 40], dtype=np.uint8)

        # Check grid lines are present at specific locations based on the formula
        grid_size = max(15, int(70 - intensity * 50)) # 70 - 25 = 45

        # Grid lines should be rendered exactly at indices that are multiples of grid_size
        self.assertTrue(np.all(result[0, 0] == grid_color))
        self.assertTrue(np.all(result[grid_size, 0] == grid_color))
        self.assertTrue(np.all(result[0, grid_size] == grid_color))

        # Points inside the grid square should remain the background color
        bg_color = np.array([150, 50, 20], dtype=np.uint8)
        self.assertTrue(np.all(result[grid_size // 2, grid_size // 2] == bg_color))

    def test_apply_blueprint_with_edges(self):
        # Create an image with a sharp vertical edge (left black, right white)
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, 50:] = 255

        intensity = 0.0
        result = apply_blueprint(frame, intensity)

        # The background without edge is (150, 50, 20)
        bg_color = np.array([150, 50, 20], dtype=np.uint8)

        # Far from the edge, it should be background color
        self.assertTrue(np.all(result[0, 0] == bg_color))
        self.assertTrue(np.all(result[50, 10] == bg_color))
        self.assertTrue(np.all(result[50, 90] == bg_color))

        # Near the edge (e.g. at x=48 or 49 due to blurring and Laplacian),
        # the color should have the edge line overlaid (white edges -> 255)
        # Check at least one pixel on the edge line is bright/white.
        edge_pixel = result[50, 48]
        self.assertTrue(np.all(edge_pixel == 255))

if __name__ == '__main__':
    unittest.main()
