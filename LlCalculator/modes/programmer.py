"""Programmer calculator mode."""

from typing import Dict, Tuple
from .base_mode import BaseMode


class ProgrammerMode(BaseMode):
    """Calculator for programmers: bases, bitwise operations, word sizes."""

    WORD_SIZES = [8, 16, 32, 64]
    BASES = {"BIN": 2, "OCT": 8, "DEC": 10, "HEX": 16}

    def __init__(self, engine):
        super().__init__("Programador", engine)
        self.word_size = 32
        self.signed = True
        self.current_value = 0
        self.pending_op = None
        self.pending_value = None
        self.input_buffer = "0"
        self.current_base = 10

    def evaluate(self, expression: str) -> str:
        # Programmer mode manages state internally
        return self.input_buffer

    def get_buttons(self) -> list:
        return [
            [("AND", "bit", "&"), ("OR", "bit", "|"), ("XOR", "bit", "^"),
             ("NOT", "bit", "~"), ("NAND", "bit", "NAND")],
            [("<<", "bit", "<<"), (">>", "bit", ">>"), ("ROL", "bit", "ROL"),
             ("ROR", "bit", "ROR"), ("XOR", "bit", "XOR")],
            [("A", "hex", "A"), ("B", "hex", "B"), ("C", "hex", "C"),
             ("D", "hex", "D"), ("E", "hex", "E")],
            [("F", "hex", "F"), ("CE", "clear", "CE"), ("C", "clear", "C"),
             ("⌫", "clear", "DEL"), ("÷", "op", "/")],
            [("7", "num", "7"), ("8", "num", "8"), ("9", "num", "9"),
             ("×", "op", "*"), ("-", "op", "-")],
            [("4", "num", "4"), ("5", "num", "5"), ("6", "num", "6"),
             ("+", "op", "+"), ("=", "eq", "=")],
            [("1", "num", "1"), ("2", "num", "2"), ("3", "num", "3"),
             ("0", "num", "0"), ("=", "eq", "=")],
        ]

    def set_word_size(self, size: int):
        if size in self.WORD_SIZES:
            self.word_size = size
            self.current_value = self._mask(self.current_value)

    def set_base(self, base: int):
        self.current_base = base
        self.input_buffer = self.to_base(self.current_value, base)

    def set_signed(self, signed: bool):
        self.signed = signed

    def input_digit(self, digit: str):
        """Append a digit in current base."""
        if self.input_buffer == "0":
            self.input_buffer = digit
        else:
            self.input_buffer += digit
        try:
            self.current_value = self._mask(int(self.input_buffer, self.current_base))
        except ValueError:
            pass

    def delete_digit(self):
        if len(self.input_buffer) > 1:
            self.input_buffer = self.input_buffer[:-1]
        else:
            self.input_buffer = "0"
        try:
            self.current_value = self._mask(int(self.input_buffer, self.current_base))
        except ValueError:
            self.current_value = 0

    def clear(self):
        self.input_buffer = "0"
        self.current_value = 0
        self.pending_op = None
        self.pending_value = None

    def clear_entry(self):
        self.input_buffer = "0"
        self.current_value = 0

    def to_base(self, value: int, base: int) -> str:
        """Convert current value to string in given base."""
        value = self._mask(value)
        if base == 2:
            return bin(value)[2:].zfill(self.word_size)
        elif base == 8:
            return oct(value)[2:]
        elif base == 10:
            if self.signed:
                return str(self._to_signed(value))
            return str(value)
        elif base == 16:
            return hex(value)[2:].upper()
        return str(value)

    def get_all_bases(self) -> Dict[str, str]:
        """Return representation in all bases."""
        return {
            "BIN": self.to_base(self.current_value, 2),
            "OCT": self.to_base(self.current_value, 8),
            "DEC": self.to_base(self.current_value, 10),
            "HEX": self.to_base(self.current_value, 16),
        }

    def _mask(self, value: int) -> int:
        """Mask value to current word size."""
        return value & ((1 << self.word_size) - 1)

    def _to_signed(self, value: int) -> int:
        """Convert unsigned masked value to signed."""
        if value & (1 << (self.word_size - 1)):
            return value - (1 << self.word_size)
        return value

    def _from_signed(self, value: int) -> int:
        """Convert signed value to unsigned masked representation."""
        if value < 0:
            return (1 << self.word_size) + value
        return self._mask(value)

    def apply_unary(self, op: str) -> str:
        """Apply unary bitwise operation."""
        val = self.current_value
        if op == "~":
            val = self._mask(~val)
        elif op == "ROL":
            msb = (val >> (self.word_size - 1)) & 1
            val = self._mask((val << 1) | msb)
        elif op == "ROR":
            lsb = val & 1
            val = self._mask((val >> 1) | (lsb << (self.word_size - 1)))
        self.current_value = val
        self.input_buffer = self.to_base(val, self.current_base)
        return self.input_buffer

    def apply_binary(self, op: str, other_value: int) -> str:
        """Apply binary bitwise operation."""
        a = self.current_value
        b = self._mask(other_value)
        if op == "&":
            res = a & b
        elif op == "|":
            res = a | b
        elif op == "^":
            res = a ^ b
        elif op == "NAND":
            res = self._mask(~(a & b))
        elif op == "NOR":
            res = self._mask(~(a | b))
        elif op == "<<":
            res = self._mask(a << b)
        elif op == ">>":
            if self.signed:
                # Arithmetic shift: preserve sign bit
                signed_a = self._to_signed(a)
                res = self._from_signed(signed_a >> b)
            else:
                res = a >> b
        elif op == "+":
            res = self._mask(a + b)
        elif op == "-":
            res = self._mask(a - b)
        elif op == "*":
            res = self._mask(a * b)
        elif op == "/":
            if b == 0:
                return "Error: División por cero"
            if self.signed:
                res = self._from_signed(self._to_signed(a) // self._to_signed(b))
            else:
                res = a // b
        elif op == "%":
            if b == 0:
                return "Error: Módulo por cero"
            if self.signed:
                res = self._from_signed(self._to_signed(a) % self._to_signed(b))
            else:
                res = a % b
        else:
            res = a
        self.current_value = self._mask(res)
        self.input_buffer = self.to_base(self.current_value, self.current_base)
        return self.input_buffer

    def prepare_operation(self, op: str):
        """Store current value and operation for next input."""
        self.pending_op = op
        self.pending_value = self.current_value
        self.input_buffer = "0"

    def execute_pending(self):
        """Execute pending operation with current value."""
        if self.pending_op and self.pending_value is not None:
            result = self.apply_binary(self.pending_op, self.current_value)
            self.pending_op = None
            self.pending_value = None
            return result
        return self.input_buffer
