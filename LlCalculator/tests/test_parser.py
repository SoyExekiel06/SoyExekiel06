"""Tests for the expression parser."""

import pytest
import math
from core.parser import ExpressionParser
from core.errors import CalculatorError, DivisionByZeroError, DomainError


class TestParserBasic:
    def test_addition(self):
        p = ExpressionParser()
        assert p.parse("2 + 3") == 5.0

    def test_precedence(self):
        p = ExpressionParser()
        assert p.parse("2 + 3 * 4") == 14.0

    def test_parentheses(self):
        p = ExpressionParser()
        assert p.parse("(2 + 3) * 4") == 20.0

    def test_subtraction(self):
        p = ExpressionParser()
        assert p.parse("10 - 4") == 6.0

    def test_division(self):
        p = ExpressionParser()
        assert p.parse("10 / 2") == 5.0

    def test_division_by_zero(self):
        p = ExpressionParser()
        with pytest.raises(DivisionByZeroError):
            p.parse("10 / 0")

    def test_power(self):
        p = ExpressionParser()
        assert p.parse("2 ^ 10") == 1024.0

    def test_modulo(self):
        p = ExpressionParser()
        assert p.parse("10 % 3") == 1.0


class TestParserFunctions:
    def test_sqrt(self):
        p = ExpressionParser()
        assert p.parse("sqrt(25)") == 5.0

    def test_sqrt_negative(self):
        p = ExpressionParser()
        with pytest.raises(DomainError):
            p.parse("sqrt(-1)")

    def test_sin_degrees(self):
        p = ExpressionParser("degrees")
        assert abs(p.parse("sin(30)") - 0.5) < 1e-10

    def test_cos_radians(self):
        p = ExpressionParser("radians")
        assert abs(p.parse("cos(0)") - 1.0) < 1e-10

    def test_ln(self):
        p = ExpressionParser()
        assert abs(p.parse("ln(e)") - 1.0) < 1e-10

    def test_log10(self):
        p = ExpressionParser()
        assert p.parse("log10(100)") == 2.0

    def test_factorial(self):
        p = ExpressionParser()
        assert p.parse("5!") == 120.0

    def test_abs(self):
        p = ExpressionParser()
        assert p.parse("abs(-5)") == 5.0

    def test_floor(self):
        p = ExpressionParser()
        assert p.parse("floor(3.7)") == 3.0

    def test_ceil(self):
        p = ExpressionParser()
        assert p.parse("ceil(3.2)") == 4.0


class TestParserConstants:
    def test_pi(self):
        p = ExpressionParser()
        assert abs(p.parse("pi") - math.pi) < 1e-10

    def test_e(self):
        p = ExpressionParser()
        assert abs(p.parse("e") - math.e) < 1e-10


class TestParserComplex:
    def test_nested_expression(self):
        p = ExpressionParser()
        result = p.parse("2 + 3 * (4 - 1)")
        assert result == 11.0

    def test_trigonometric_with_arithmetic(self):
        p = ExpressionParser("degrees")
        result = p.parse("sqrt(25) + sin(30)")
        assert abs(result - 5.5) < 1e-10

    def test_combinatorics(self):
        p = ExpressionParser()
        assert p.parse("nCr(5, 2)") == 10.0
        assert p.parse("nPr(5, 2)") == 20.0
