import unittest
from unittest.mock import Mock, patch
import sys

# Mock pygame and config before importing ui
class MockRect:
    def __init__(self, x=0, y=0, w=0, h=0, **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = w
        self.height = h
        self.left = x
        self.right = x + w
        self.top = y
        self.bottom = y + h

    def collidepoint(self, pos):
        return False

mock_pygame = Mock()
mock_pygame.Rect = MockRect
mock_pygame.font = Mock()
mock_pygame.font.SysFont = Mock()
sys.modules['pygame'] = mock_pygame

mock_config = Mock()
mock_config.PANEL_WIDTH = 200
mock_config.PANEL_BG = (0,0,0)
mock_config.PANEL_BORDER = (0,0,0)
mock_config.ACTIVE_HIGHLIGHT = (0,0,0)
sys.modules['config'] = mock_config

from ui import FilterPanel

class DummyFilter:
    def __init__(self, name, intensity=0.5):
        self.name = name
        self.intensity = intensity

class TestFilterPanelApplyInputText(unittest.TestCase):
    def setUp(self):
        # Create a mock font
        mock_font = Mock()

        # Create dummy filters
        self.filters = [
            DummyFilter("Filter 1", 0.5),
            DummyFilter("Filter 2", 0.8)
        ]

        # Initialize FilterPanel
        self.panel = FilterPanel(self.filters, mock_font, 800, 600)

    def test_apply_input_text_empty(self):
        self.panel.active_idx = 0
        self.panel.input_text = ""
        self.panel.apply_input_text()
        self.assertEqual(self.panel.filters[0].intensity, 0.0)

    def test_apply_input_text_valid_int(self):
        self.panel.active_idx = 0
        self.panel.input_text = "75"
        self.panel.apply_input_text()
        self.assertEqual(self.panel.filters[0].intensity, 0.75)

    def test_apply_input_text_invalid_string(self):
        self.panel.active_idx = 1
        self.panel.filters[1].intensity = 0.8 # Initial intensity
        self.panel.input_text = "abc"
        self.panel.apply_input_text()
        # Should fallback to current intensity
        self.assertEqual(self.panel.filters[1].intensity, 0.8)

    def test_apply_input_text_below_zero(self):
        self.panel.active_idx = 0
        self.panel.input_text = "-10"
        self.panel.apply_input_text()
        self.assertEqual(self.panel.filters[0].intensity, 0.0)

    def test_apply_input_text_above_100(self):
        self.panel.active_idx = 0
        self.panel.input_text = "150"
        self.panel.apply_input_text()
        self.assertEqual(self.panel.filters[0].intensity, 1.0)

    def test_apply_input_text_no_active_filter(self):
        self.panel.active_idx = -1
        self.panel.input_text = "50"
        self.panel.apply_input_text()
        # Ensure no crash and intensities remain unchanged
        self.assertEqual(self.panel.filters[0].intensity, 0.5)
        self.assertEqual(self.panel.filters[1].intensity, 0.8)

if __name__ == '__main__':
    unittest.main()
