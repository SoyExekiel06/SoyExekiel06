"""Recursive Descent Parser for mathematical expressions.

Evaluates expressions safely without using eval().
Supports operator precedence, unary operators, functions and constants.
"""

import math
from typing import List, Callable

from .tokenizer import Tokenizer, Token, TokenType
from .errors import SyntaxCalcError, DomainError, DivisionByZeroError, OverflowCalcError
from .constants import MathConstants


class ExpressionParser:
    """Parses and evaluates mathematical expressions."""

    def __init__(self, angle_mode: str = "degrees"):
        self.angle_mode = angle_mode  # "degrees", "radians", "gradians"
        self.tokens: List[Token] = []
        self.pos = 0

    def parse(self, expression: str) -> float:
        tokenizer = Tokenizer(expression)
        self.tokens = tokenizer.tokenize()
        self.pos = 0
        result = self._expression()
        self._expect(TokenType.EOF)
        return result

    # Grammar methods
    def _expression(self) -> float:
        """expression → term ((+|-) term)*"""
        value = self._term()
        while self._current().value in ("+", "-"):
            op = self._advance().value
            right = self._term()
            if op == "+":
                value = value + right
            else:
                value = value - right
        return value

    def _term(self) -> float:
        """term → factor ((*|/|%) factor)*"""
        value = self._factor()
        while self._current().value in ("*", "/", "%"):
            op = self._advance().value
            right = self._factor()
            if op == "*":
                value = value * right
            elif op == "/":
                if right == 0:
                    raise DivisionByZeroError("División por cero")
                value = value / right
            elif op == "%":
                if right == 0:
                    raise DivisionByZeroError("Módulo por cero")
                value = value % right
        return value

    def _factor(self) -> float:
        """factor → power (^ power)*  (right-associative via recursion)"""
        left = self._power()
        if self._current().value == "^":
            self._advance()
            right = self._factor()  # right associative
            # Handle negative bases with fractional exponents
            try:
                left = math.pow(left, right)
            except ValueError as exc:
                raise DomainError(f"Potencia inválida: {exc}")
            except OverflowError as exc:
                raise OverflowCalcError(f"Desbordamiento en potencia: {exc}")
        return left

    def _power(self) -> float:
        """power → unary"""
        return self._unary()

    def _unary(self) -> float:
        """unary → (+|-) unary | postfix"""
        if self._current().value in ("+", "-"):
            op = self._advance().value
            operand = self._unary()
            return operand if op == "+" else -operand
        return self._postfix()

    def _postfix(self) -> float:
        """postfix → primary (!)?"""
        value = self._primary()
        if self._current().value == "!":
            self._advance()
            if value < 0 or not float(value).is_integer():
                raise DomainError("Factorial solo definido para enteros no negativos")
            n = int(value)
            try:
                value = math.factorial(n)
            except OverflowError as exc:
                raise OverflowCalcError(f"Desbordamiento en factorial: {exc}")
        return value

    def _primary(self) -> float:
        """primary → number | constant | function | ( expression )"""
        token = self._current()

        if token.type == TokenType.NUMBER:
            self._advance()
            return float(token.value)

        if token.type == TokenType.CONSTANT:
            self._advance()
            if token.value == "pi":
                return MathConstants.PI
            elif token.value == "e":
                return MathConstants.E
            elif token.value == "phi":
                return MathConstants.PHI

        if token.type == TokenType.FUNCTION:
            return self._function()

        if token.type == TokenType.LPAREN:
            self._advance()
            value = self._expression()
            self._expect(TokenType.RPAREN)
            return value

        raise SyntaxCalcError(f"Token inesperado '{token.value}' en posición {token.pos}")

    def _function(self) -> float:
        """Evaluate a function call."""
        func_token = self._advance()
        name = func_token.value

        self._expect(TokenType.LPAREN)

        # Special cases with multiple arguments
        if name in ("nCr", "nPr"):
            arg1 = self._expression()
            self._expect(TokenType.COMMA)
            arg2 = self._expression()
            self._expect(TokenType.RPAREN)
            if not (float(arg1).is_integer() and float(arg2).is_integer()):
                raise DomainError("nCr y nPr requieren enteros")
            n, r = int(arg1), int(arg2)
            if n < 0 or r < 0 or r > n:
                raise DomainError("Argumentos inválidos para combinatoria")
            if name == "nCr":
                return math.comb(n, r)
            else:
                return math.perm(n, r)

        if name == "log":
            # log(x, base) or log(x) default base 10
            arg1 = self._expression()
            if self._current().type == TokenType.COMMA:
                self._advance()
                base_val = self._expression()
                self._expect(TokenType.RPAREN)
                if arg1 <= 0 or base_val <= 0 or base_val == 1:
                    raise DomainError("Logaritmo inválido")
                return math.log(arg1, base_val)
            self._expect(TokenType.RPAREN)
            if arg1 <= 0:
                raise DomainError("Logaritmo de número no positivo")
            return math.log10(arg1)

        # Single-argument functions
        arg = self._expression()
        self._expect(TokenType.RPAREN)
        return self._apply_function(name, arg)

    def _apply_function(self, name: str, x: float) -> float:
        """Apply a single-argument mathematical function."""
        funcs: dict[str, Callable[[float], float]] = {
            "sqrt": lambda v: math.sqrt(v) if v >= 0 else (_ for _ in ()).throw(DomainError("Raíz de número negativo")),
            "ln": lambda v: math.log(v) if v > 0 else (_ for _ in ()).throw(DomainError("Logaritmo de número no positivo")),
            "log10": lambda v: math.log10(v) if v > 0 else (_ for _ in ()).throw(DomainError("Logaritmo de número no positivo")),
            "log2": lambda v: math.log2(v) if v > 0 else (_ for _ in ()).throw(DomainError("Logaritmo de número no positivo")),
            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,
            "round": round,
            "exp": math.exp,
        }

        if name in funcs:
            try:
                return funcs[name](x)
            except ValueError as exc:
                raise DomainError(str(exc))
            except OverflowError as exc:
                raise OverflowCalcError(str(exc))

        # Trigonometric functions need angle conversion
        trig_funcs = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "asinh": math.asinh, "acosh": math.acosh, "atanh": math.atanh,
        }

        if name in trig_funcs:
            return self._apply_trig(name, x)

        raise SyntaxCalcError(f"Función desconocida: {name}")

    def _apply_trig(self, name: str, x: float) -> float:
        """Apply trigonometric functions with angle mode handling."""
        import math

        # Inverse hyperbolic
        if name in ("asinh", "acosh", "atanh"):
            if name == "acosh" and x < 1:
                raise DomainError("acosh requiere x >= 1")
            if name == "atanh" and not (-1 < x < 1):
                raise DomainError("atanh requiere -1 < x < 1")
            return getattr(math, name)(x)

        # Hyperbolic direct
        if name in ("sinh", "cosh", "tanh"):
            try:
                return getattr(math, name)(x)
            except OverflowError as exc:
                raise OverflowCalcError(str(exc))

        # Inverse trig
        if name in ("asin", "acos"):
            if not (-1 <= x <= 1):
                raise DomainError(f"{name} requiere -1 <= x <= 1")
            result = getattr(math, name)(x)
            return self._from_radians(result)

        if name == "atan":
            result = math.atan(x)
            return self._from_radians(result)

        # Direct trig: convert input to radians first
        rad = self._to_radians(x)
        if name == "tan":
            # Check for asymptotes near pi/2 + k*pi
            cos_val = math.cos(rad)
            if abs(cos_val) < 1e-15:
                raise DomainError("tan indefinido en este ángulo")
        try:
            return getattr(math, name)(rad)
        except ValueError as exc:
            raise DomainError(str(exc))

    def _to_radians(self, value: float) -> float:
        if self.angle_mode == "degrees":
            return math.radians(value)
        elif self.angle_mode == "gradians":
            return value * math.pi / 200
        return value

    def _from_radians(self, value: float) -> float:
        if self.angle_mode == "degrees":
            return math.degrees(value)
        elif self.angle_mode == "gradians":
            return value * 200 / math.pi
        return value

    # Helper methods
    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def _expect(self, token_type: TokenType):
        if self._current().type != token_type:
            raise SyntaxCalcError(
                f"Se esperaba {token_type.name} pero se encontró {self._current().value}"
            )
        self._advance()
