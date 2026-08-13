"""Tests for programmer mode."""

from modes.programmer import ProgrammerMode
from core.engine import CalculatorEngine


class TestProgrammerMode:
    def setup_method(self):
        self.engine = CalculatorEngine()
        self.mode = ProgrammerMode(self.engine)

    def test_input_and_display(self):
        self.mode.set_base(10)
        self.mode.input_digit("2")
        self.mode.input_digit("5")
        self.mode.input_digit("5")
        values = self.mode.get_all_bases()
        assert values["DEC"] == "255"
        assert values["HEX"] == "FF"

    def test_bitwise_and(self):
        self.mode.set_base(10)
        self.mode.current_value = 0b1100
        self.mode.prepare_operation("&")
        self.mode.current_value = 0b1010
        self.mode.execute_pending()
        assert self.mode.current_value == 0b1000

    def test_bitwise_or(self):
        self.mode.set_base(10)
        self.mode.current_value = 0b1100
        self.mode.prepare_operation("|")
        self.mode.current_value = 0b1010
        self.mode.execute_pending()
        assert self.mode.current_value == 0b1110

    def test_shift_left(self):
        self.mode.set_base(10)
        self.mode.current_value = 1
        self.mode.prepare_operation("<<")
        self.mode.current_value = 3
        self.mode.execute_pending()
        assert self.mode.current_value == 8

    def test_word_size_mask(self):
        self.mode.set_word_size(8)
        self.mode.current_value = 256
        masked = self.mode._mask(256)
        assert masked == 0

    def test_signed_conversion(self):
        self.mode.set_word_size(8)
        self.mode.signed = True
        unsigned = self.mode._from_signed(-1)
        assert unsigned == 255
        signed_back = self.mode._to_signed(255)
        assert signed_back == -1
