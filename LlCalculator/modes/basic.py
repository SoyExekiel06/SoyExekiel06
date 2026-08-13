"""Basic calculator mode."""

from .base_mode import BaseMode


class BasicMode(BaseMode):
    """Standard arithmetic calculator."""

    def __init__(self, engine):
        super().__init__("Básico", engine)

    def evaluate(self, expression: str) -> str:
        return self.engine.evaluate(expression)

    def get_buttons(self) -> list:
        """Return button layout as list of rows.

        Each row is a list of tuples: (label, type, action/data)
        Types: 'num', 'op', 'func', 'mem', 'clear', 'eq', 'paren'
        """
        return [
            [("MC", "mem", "MC"), ("MR", "mem", "MR"), ("M+", "mem", "M+"),
             ("M-", "mem", "M-"), ("MS", "mem", "MS")],
            [("C", "clear", "C"), ("CE", "clear", "CE"), ("⌫", "clear", "DEL"),
             ("÷", "op", "/"), ("×", "op", "*")],
            [("7", "num", "7"), ("8", "num", "8"), ("9", "num", "9"),
             ("-", "op", "-"), ("+", "op", "+")],
            [("4", "num", "4"), ("5", "num", "5"), ("6", "num", "6"),
             ("%", "op", "%"), ("±", "func", "neg")],
            [("1", "num", "1"), ("2", "num", "2"), ("3", "num", "3"),
             ("(", "paren", "("), (")", "paren", ")")],
            [("0", "num", "0"), (",", "num", "."), ("=", "eq", "="),],
        ]
