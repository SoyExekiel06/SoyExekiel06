class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero occurs."""
    pass


class DomainError(CalculatorError):
    """Raised when a mathematical function receives an invalid domain value."""
    pass


class SyntaxCalcError(CalculatorError):
    """Raised when the expression has invalid syntax."""
    pass


class OverflowCalcError(CalculatorError):
    """Raised when a numeric overflow occurs."""
    pass
