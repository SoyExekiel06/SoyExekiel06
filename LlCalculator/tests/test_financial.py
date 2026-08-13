"""Tests for financial mode."""

from modes.financial import FinancialMode
from core.engine import CalculatorEngine


class TestFinancialMode:
    def setup_method(self):
        self.engine = CalculatorEngine()
        self.mode = FinancialMode(self.engine)

    def test_simple_interest(self):
        result = self.mode.simple_interest(1000, 5, 2)
        assert result["interest"] == 100.0
        assert result["final_amount"] == 1100.0

    def test_compound_interest(self):
        result = self.mode.compound_interest(1000, 5, 2, 1)
        assert result["final_amount"] > 1100

    def test_loan_payment(self):
        result = self.mode.loan_payment(100000, 5, 30)
        assert result["payment"] > 0
        assert result["total_paid"] > 100000

    def test_present_value(self):
        result = self.mode.present_value(1100, 10, 1)
        assert abs(result["present_value"] - 1000) < 1

    def test_future_value(self):
        result = self.mode.future_value(1000, 10, 1)
        assert abs(result["future_value"] - 1100) < 1

    def test_percentage_change(self):
        result = self.mode.percentage_change(100, 150)
        assert result["change_percent"] == 50.0

    def test_discount(self):
        result = self.mode.discount(200, 10)
        assert result["discount_amount"] == 20.0
        assert result["final_price"] == 180.0
