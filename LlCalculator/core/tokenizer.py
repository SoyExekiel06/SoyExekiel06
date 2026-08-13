"""Tokenizer for mathematical expressions.

Converts a raw expression string into a list of typed tokens.
Supports numbers, operators, functions, constants and parentheses.
"""

import re
from enum import Enum, auto
from typing import List, NamedTuple


class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    FUNCTION = auto()
    CONSTANT = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    EOF = auto()


class Token(NamedTuple):
    type: TokenType
    value: str
    pos: int


class Tokenizer:
    # Order matters: functions before single-letter constants
    FUNCTION_NAMES = [
        "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
        "asin", "acos", "atan",
        "sin", "cos", "tan",
        "sqrt", "log2", "log10", "log", "ln",
        "abs", "floor", "ceil", "round", "exp",
        "nCr", "nPr",
    ]
    CONSTANTS = ["pi", "e", "phi"]
    OPERATORS = ["+", "-", "*", "/", "%", "^", "!"]

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < self.length:
            ch = self.text[self.pos]

            if ch.isspace():
                self.pos += 1
                continue

            if ch == "(":
                tokens.append(Token(TokenType.LPAREN, ch, self.pos))
                self.pos += 1
                continue

            if ch == ")":
                tokens.append(Token(TokenType.RPAREN, ch, self.pos))
                self.pos += 1
                continue

            if ch == ",":
                tokens.append(Token(TokenType.COMMA, ch, self.pos))
                self.pos += 1
                continue

            # Numbers: integers, decimals, scientific notation
            num_match = re.match(r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?", self.text[self.pos:])
            if num_match:
                value = num_match.group(0)
                tokens.append(Token(TokenType.NUMBER, value, self.pos))
                self.pos += len(value)
                continue

            # Functions and constants (case-insensitive for functions)
            word_match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", self.text[self.pos:])
            if word_match:
                word = word_match.group(0)
                lower = word.lower()
                if lower in [f.lower() for f in self.FUNCTION_NAMES]:
                    # Store canonical name
                    canonical = next(f for f in self.FUNCTION_NAMES if f.lower() == lower)
                    tokens.append(Token(TokenType.FUNCTION, canonical, self.pos))
                elif lower in [c.lower() for c in self.CONSTANTS]:
                    canonical = next(c for c in self.CONSTANTS if c.lower() == lower)
                    tokens.append(Token(TokenType.CONSTANT, canonical, self.pos))
                else:
                    raise ValueError(f"Unknown identifier '{word}' at position {self.pos}")
                self.pos += len(word)
                continue

            # Operators (including multi-char like ** if needed, but we stick to single)
            if ch in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, ch, self.pos))
                self.pos += 1
                continue

            raise ValueError(f"Unexpected character '{ch}' at position {self.pos}")

        tokens.append(Token(TokenType.EOF, "", self.pos))
        return tokens
