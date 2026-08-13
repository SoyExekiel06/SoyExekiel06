"""Calculator Engine.

Orchestrates parsing, evaluation, and mode-specific logic.
Acts as the bridge between UI and mathematical core.
"""

from typing import Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from .parser import ExpressionParser
from .errors import CalculatorError


class CalculatorEngine:
    """Main calculation engine."""

    def __init__(self, angle_mode: str = "degrees", precision: int = 10):
        self.angle_mode = angle_mode
        self.precision = precision
        self.parser = ExpressionParser(angle_mode=angle_mode)
        self.last_result: Optional[float] = None
        self.error_state = False

    def set_angle_mode(self, mode: str):
        """Update angle mode (degrees, radians, gradians)."""
        self.angle_mode = mode
        self.parser.angle_mode = mode

    def set_precision(self, precision: int):
        """Update display precision."""
        self.precision = precision

    def evaluate(self, expression: str) -> str:
        """Evaluate an expression and return formatted result."""
        self.error_state = False
        try:
            result = self.parser.parse(expression)
            self.last_result = result
            return self._format_result(result)
        except CalculatorError as exc:
            self.error_state = True
            self.last_result = None
            return f"Error: {exc}"
        except Exception as exc:
            self.error_state = True
            self.last_result = None
            return f"Error: {exc}"

    def _format_result(self, value: float) -> str:
        """Format numeric result according to precision settings."""
        if self.precision < 0:
            # Auto: strip trailing zeros
            s = f"{value:.15g}"
            return s
        try:
            d = Decimal(str(value))
            # Quantize to desired precision
            exp = Decimal(1) / (Decimal(10) ** self.precision)
            quantized = d.quantize(exp, rounding=ROUND_HALF_UP)
            # Normalize to strip trailing zeros if integer
            normalized = quantized.normalize()
            return str(normalized)
        except InvalidOperation:
            return str(value)

    def get_last_result_value(self) -> Optional[float]:
        return self.last_result

    def is_error(self) -> bool:
        return self.error_state
