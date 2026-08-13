"""Tests for advanced mode."""

from modes.advanced import AdvancedMode
from core.engine import CalculatorEngine
import math


class TestAdvancedMode:
    def setup_method(self):
        self.engine = CalculatorEngine(angle_mode="degrees")
        self.mode = AdvancedMode(self.engine)

    def test_trigonometry(self):
        result = self.mode.evaluate("sin(30)")
        assert abs(float(result) - 0.5) < 1e-10

    def test_logarithms(self):
        result = self.mode.evaluate("log10(1000)")
        assert float(result) == 3.0

    def test_hyperbolic(self):
        result = self.mode.evaluate("sinh(0)")
        assert float(result) == 0.0
