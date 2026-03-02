import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import cv2
from filters import apply_ascii_contrast

class TestFilters(unittest.TestCase):
    @patch('cv2.createCLAHE')
    @patch('cv2.convertScaleAbs')
    def test_apply_ascii_contrast_normal(self, mock_convertScaleAbs, mock_createCLAHE):
        mock_clahe_instance = MagicMock()
        mock_createCLAHE.return_value = mock_clahe_instance

        expected_enhanced = np.zeros((10, 10), dtype=np.uint8)
        mock_clahe_instance.apply.return_value = expected_enhanced

        expected_result = np.ones((10, 10), dtype=np.uint8)
        mock_convertScaleAbs.return_value = expected_result

        gray_frame = np.zeros((10, 10), dtype=np.uint8)
        intensity = 0.5

        result = apply_ascii_contrast(gray_frame, intensity)

        expected_limit = 1.0 + (0.5 * 4.0)
        expected_alpha = 1.0 + (0.5 * 1.5)
        expected_beta = (0.5 - 0.5) * 50

        mock_createCLAHE.assert_called_once_with(clipLimit=expected_limit, tileGridSize=(8, 8))
        mock_clahe_instance.apply.assert_called_once_with(gray_frame)
        mock_convertScaleAbs.assert_called_once_with(expected_enhanced, alpha=expected_alpha, beta=expected_beta)
        self.assertIs(result, expected_result)

    @patch('cv2.createCLAHE')
    @patch('cv2.convertScaleAbs')
    def test_apply_ascii_contrast_zero_intensity(self, mock_convertScaleAbs, mock_createCLAHE):
        mock_clahe_instance = MagicMock()
        mock_createCLAHE.return_value = mock_clahe_instance

        expected_enhanced = np.zeros((10, 10), dtype=np.uint8)
        mock_clahe_instance.apply.return_value = expected_enhanced

        expected_result = np.ones((10, 10), dtype=np.uint8)
        mock_convertScaleAbs.return_value = expected_result

        gray_frame = np.zeros((10, 10), dtype=np.uint8)
        intensity = 0.0

        result = apply_ascii_contrast(gray_frame, intensity)

        expected_limit = 1.0 + (0.0 * 4.0)
        expected_alpha = 1.0 + (0.0 * 1.5)
        expected_beta = (0.0 - 0.5) * 50

        mock_createCLAHE.assert_called_once_with(clipLimit=expected_limit, tileGridSize=(8, 8))
        mock_clahe_instance.apply.assert_called_once_with(gray_frame)
        mock_convertScaleAbs.assert_called_once_with(expected_enhanced, alpha=expected_alpha, beta=expected_beta)
        self.assertIs(result, expected_result)

    @patch('cv2.createCLAHE')
    @patch('cv2.convertScaleAbs')
    def test_apply_ascii_contrast_max_intensity(self, mock_convertScaleAbs, mock_createCLAHE):
        mock_clahe_instance = MagicMock()
        mock_createCLAHE.return_value = mock_clahe_instance

        expected_enhanced = np.zeros((10, 10), dtype=np.uint8)
        mock_clahe_instance.apply.return_value = expected_enhanced

        expected_result = np.ones((10, 10), dtype=np.uint8)
        mock_convertScaleAbs.return_value = expected_result

        gray_frame = np.zeros((10, 10), dtype=np.uint8)
        intensity = 1.0

        result = apply_ascii_contrast(gray_frame, intensity)

        expected_limit = 1.0 + (1.0 * 4.0)
        expected_alpha = 1.0 + (1.0 * 1.5)
        expected_beta = (1.0 - 0.5) * 50

        mock_createCLAHE.assert_called_once_with(clipLimit=expected_limit, tileGridSize=(8, 8))
        mock_clahe_instance.apply.assert_called_once_with(gray_frame)
        mock_convertScaleAbs.assert_called_once_with(expected_enhanced, alpha=expected_alpha, beta=expected_beta)
        self.assertIs(result, expected_result)

if __name__ == '__main__':
    unittest.main()
