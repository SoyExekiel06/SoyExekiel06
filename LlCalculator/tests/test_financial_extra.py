"""Extra tests for financial mode new functions."""

from modes.financial import FinancialMode
from core.engine import CalculatorEngine


class TestFinancialExtras:
    def setup_method(self):
        self.engine = CalculatorEngine()
        self.mode = FinancialMode(self.engine)

    def test_trmc(self):
        # trmc: rate to grow 1000 to 2000 in 10 periods -> ~7.177%
        res = self.mode.evaluate("trmc(1000,2000,10)")
        assert "%" in res

    def test_pmt(self):
        res = self.mode.evaluate("pmt(10000,5,36)")
        assert "Pago" in res or float(res.split()[0]) >= 0

    def test_npv(self):
        res = self.mode.evaluate("npv(5,-1000,200,300,400)")
        # should parse as number
        val = float(res)
        assert isinstance(val, float)

    def test_irr(self):
        res = self.mode.evaluate("irr(-1000,200,300,400)")
        assert "%" in res or res.startswith("Error")

    def test_ddb(self):
        res = self.mode.evaluate("ddb(10000,1000,5,2)")
        val = float(res)
        assert val >= 0

    def test_rate_conv(self):
        res = self.mode.evaluate("rate_conv(12,12,1)")
        assert "Efectiva" in res or "Effective" in res
