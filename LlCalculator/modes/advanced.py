"""Advanced (Scientific) calculator mode."""

from .base_mode import BaseMode


class AdvancedMode(BaseMode):
    """Scientific calculator with trigonometry, logarithms, etc."""

    def __init__(self, engine):
        super().__init__("Avanzado", engine)

    def evaluate(self, expression: str) -> str:
        return self.engine.evaluate(expression)

    def get_buttons(self) -> list:
        return [
            [("MC", "mem", "MC"), ("MR", "mem", "MR"), ("M+", "mem", "M+"),
             ("M-", "mem", "M-"), ("MS", "mem", "MS")],
            [("sin", "func", "sin("), ("cos", "func", "cos("), ("tan", "func", "tan("),
             ("asin", "func", "asin("), ("acos", "func", "acos(")],
            [("sinh", "func", "sinh("), ("cosh", "func", "cosh("), ("tanh", "func", "tanh("),
             ("asinh", "func", "asinh("), ("acosh", "func", "acosh(")],
            [("ln", "func", "ln("), ("log", "func", "log("), ("log₂", "func", "log2("),
             ("10ˣ", "func", "10^"), ("eˣ", "func", "exp(")],
            [("x²", "func", "^2"), ("xʸ", "op", "^"), ("√", "func", "sqrt("),
             ("ⁿ√", "func", "^(1/"), ("|x|", "func", "abs(")],
            [("π", "const", "pi"), ("e", "const", "e"), ("φ", "const", "phi"),
             ("nCr", "func", "nCr("), ("nPr", "func", "nPr(")],
            [("C", "clear", "C"), ("CE", "clear", "CE"), ("⌫", "clear", "DEL"),
             ("÷", "op", "/"), ("×", "op", "*")],
            [("7", "num", "7"), ("8", "num", "8"), ("9", "num", "9"),
             ("-", "op", "-"), ("+", "op", "+")],
            [("4", "num", "4"), ("5", "num", "5"), ("6", "num", "6"),
             ("%", "op", "%"), ("!", "func", "!")],
            [("1", "num", "1"), ("2", "num", "2"), ("3", "num", "3"),
             ("(", "paren", "("), (")", "paren", ")")],
            [("0", "num", "0"), (".", "num", "."), ("=", "eq", "="),],
        ]
