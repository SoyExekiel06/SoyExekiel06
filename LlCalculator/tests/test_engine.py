"""Tests for calculator engine."""

from core.engine import CalculatorEngine


class TestEngine:
    def test_basic_evaluation(self):
        e = CalculatorEngine()
        assert e.evaluate("2 + 2") == "4"

    def test_precision_formatting(self):
        e = CalculatorEngine(precision=2)
        assert e.evaluate("1 / 3") == "0.33"

    def test_auto_precision(self):
        e = CalculatorEngine(precision=-1)
        result = e.evaluate("0.1 + 0.2")
        assert "0.3" in result

    def test_error_handling(self):
        e = CalculatorEngine()
        result = e.evaluate("10 / 0")
        assert result.startswith("Error:")

    def test_angle_mode_change(self):
        e = CalculatorEngine(angle_mode="degrees")
        e.set_angle_mode("radians")
        assert e.angle_mode == "radians"
