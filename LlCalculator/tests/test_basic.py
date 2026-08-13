"""Tests for basic mode."""

from modes.basic import BasicMode
from core.engine import CalculatorEngine


class TestBasicMode:
    def setup_method(self):
        self.engine = CalculatorEngine()
        self.mode = BasicMode(self.engine)

    def test_addition(self):
        assert self.mode.evaluate("5 + 5") == "10"

    def test_buttons_config(self):
        buttons = self.mode.get_buttons()
        assert len(buttons) > 0
