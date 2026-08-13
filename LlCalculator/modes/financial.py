"""Financial calculator mode."""

from typing import Dict, List, Tuple, Optional
from decimal import Decimal, ROUND_HALF_UP

from .base_mode import BaseMode


class FinancialMode(BaseMode):
    """Financial calculations: interest, loans, present value, etc."""

    def __init__(self, engine):
        super().__init__("Financiero", engine)

    def evaluate(self, expression: str) -> str:
        # Accept expressions of the form: func(arg1,arg2,...)
        expr = expression.strip()
        if not expr:
            return ""

        # simple dispatcher
        try:
            if expr.endswith(")") and "(" in expr:
                name, argstr = expr.split("(", 1)
                name = name.strip().lower()
                argstr = argstr[:-1]
                args = [a.strip() for a in argstr.split(",") if a.strip()]
                # allow lists for cashflows (npv/irr): if an arg contains ';' split into multiple
                parsed = []
                for a in args:
                    if ";" in a:
                        parsed.extend([float(x) for x in a.split(";") if x.strip()])
                    else:
                        parsed.append(float(a))

                if name in ("trmc", "trmci", "trm"):
                    # trmc(pv, fv, n) -> rate in percent
                    pv, fv, n = parsed[0], parsed[1], parsed[2]
                    r = (fv / pv) ** (1 / n) - 1
                    return f"{r * 100:.6f}%"

                if name in ("vf", "future_value"):
                    pv, rate, periods = parsed[0], parsed[1], parsed[2]
                    return f"{self.future_value(pv, rate, periods)['future_value']:.6f}"

                if name in ("pv", "present_value"):
                    fv, rate, periods = parsed[0], parsed[1], parsed[2]
                    return f"{self.present_value(fv, rate, periods)['present_value']:.6f}"

                if name in ("pmt", "annuity"):
                    pv, rate, periods = parsed[0], parsed[1], parsed[2]
                    return f"{self.annuity_payment(pv, rate, periods)['payment']:.6f}"

                if name in ("npv",):
                    rate = parsed[0]
                    cashflows = parsed[1:]
                    npv_val = sum(cf / ((1 + rate / 100) ** i) for i, cf in enumerate(cashflows, start=0))
                    return f"{npv_val:.6f}"

                if name in ("irr",):
                    cashflows = parsed
                    irr_val = self._irr(cashflows)
                    if irr_val is None:
                        return "Error: no converge IRR"
                    return f"{irr_val * 100:.6f}%"

                if name in ("ddb", "ddd", "dep_ddb", "depddb"):
                    # ddb(cost, salvage, life, period)
                    cost, salvage, life, period = parsed[0], parsed[1], int(parsed[2]), int(parsed[3])
                    return f"{self._ddb(cost, salvage, life, period):.6f}"

                if name in ("rate_conv",):
                    nominal, from_freq, to_freq = parsed[0], parsed[1], parsed[2]
                    conv = self.rate_conversion(nominal, from_freq, to_freq)
                    return f"Efectiva: {conv['effective_rate']:.6f}% | Nominal: {conv['converted_nominal']:.6f}%"

                if name in ("amort", "loan"):
                    principal, annual_rate, years = parsed[0], parsed[1], parsed[2]
                    res = self.loan_payment(principal, annual_rate, years)
                    return f"Pago: {res['payment']:.6f} | Interés total: {res['total_interest']:.6f}"

        except Exception as exc:
            return f"Error: argumentos inválidos ({exc})"

        # Fallback: not recognised
        return "Función financiera no reconocida"

    def get_buttons(self) -> list:
        # Financial mode: common financial functions + numeric keypad.
        # Labels use Spanish/abbreviated forms requested by the user.
        return [
            [("Trmc", "func", "trmc"), ("Ddd", "func", "ddd"), ("Vf", "func", "vf"), ("PV", "func", "pv"), ("PMT", "func", "pmt")],
            [("N", "func", "n"), ("I/Y", "func", "iy"), ("NPV", "func", "npv"), ("IRR", "func", "irr"), ("DDB", "func", "ddb")],
            [("Tasa→Efectiva", "func", "rate_conv"), ("Anual→Nominal", "func", "rate_nom"), ("Amort", "func", "amort"), ("Dep SL", "func", "dep_sl"), ("Dep DDB", "func", "dep_ddb")],
            [("7", "num", "7"), ("8", "num", "8"), ("9", "num", "9"), ("C", "clear", "C")],
            [("4", "num", "4"), ("5", "num", "5"), ("6", "num", "6"), ("CE", "clear", "CE")],
            [("1", "num", "1"), ("2", "num", "2"), ("3", "num", "3"), ("⌫", "clear", "DEL")],
            [("0", "num", "0"), (".", "num", "."), ("=", "eq", "="),],
        ]

    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> Dict[str, float]:
        """Calculate simple interest.

        Formula: I = P * r * t
        """
        interest = principal * (rate / 100) * time
        final = principal + interest
        return {
            "interest": interest,
            "final_amount": final,
            "formula": "I = P × r × t",
        }

    @staticmethod
    def compound_interest(principal: float, rate: float, periods: float,
                          frequency: float = 1.0) -> Dict[str, float]:
        """Calculate compound interest.

        Formula: A = P(1 + r/n)^(nt)
        """
        r = rate / 100
        amount = principal * ((1 + r / frequency) ** (frequency * periods))
        interest = amount - principal
        return {
            "final_amount": amount,
            "interest": interest,
            "formula": "A = P(1 + r/n)^(nt)",
        }

    @staticmethod
    def loan_payment(principal: float, annual_rate: float, years: float,
                       payments_per_year: float = 12.0) -> Dict[str, any]:
        """Calculate loan amortization.

        Formula: M = P[r(1+r)^n]/[(1+r)^n-1]
        """
        n = years * payments_per_year
        r = (annual_rate / 100) / payments_per_year
        if r == 0:
            payment = principal / n
        else:
            payment = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        total_paid = payment * n
        total_interest = total_paid - principal

        # Generate amortization schedule (first 12 and last 12 entries for display)
        schedule = []
        balance = principal
        for i in range(1, int(n) + 1):
            interest_payment = balance * r
            principal_payment = payment - interest_payment
            balance -= principal_payment
            if balance < 0:
                balance = 0
            schedule.append({
                "period": i,
                "payment": payment,
                "principal": principal_payment,
                "interest": interest_payment,
                "balance": balance,
            })

        return {
            "payment": payment,
            "total_paid": total_paid,
            "total_interest": total_interest,
            "periods": int(n),
            "schedule": schedule,
            "formula": "M = P[r(1+r)^n]/[(1+r)^n-1]",
        }

    @staticmethod
    def present_value(future_value: float, rate: float, periods: float) -> Dict[str, float]:
        """Calculate present value.

        Formula: PV = FV / (1 + r)^n
        """
        r = rate / 100
        pv = future_value / ((1 + r) ** periods)
        return {
            "present_value": pv,
            "formula": "PV = FV / (1 + r)^n",
        }

    @staticmethod
    def future_value(present_value: float, rate: float, periods: float) -> Dict[str, float]:
        """Calculate future value.

        Formula: FV = PV × (1 + r)^n
        """
        r = rate / 100
        fv = present_value * ((1 + r) ** periods)
        return {
            "future_value": fv,
            "formula": "FV = PV × (1 + r)^n",
        }

    @staticmethod
    def annuity_payment(present_value: float, rate: float, periods: float) -> Dict[str, float]:
        """Calculate annuity payment from present value.

        Formula: PMT = PV × r / (1 - (1 + r)^-n)
        """
        r = rate / 100
        if r == 0:
            pmt = present_value / periods
        else:
            pmt = present_value * r / (1 - (1 + r) ** (-periods))
        return {
            "payment": pmt,
            "formula": "PMT = PV × r / (1 - (1+r)^-n)",
        }

    @staticmethod
    def percentage_change(old_value: float, new_value: float) -> Dict[str, float]:
        """Calculate percentage change.

        Formula: ((New - Old) / Old) × 100
        """
        if old_value == 0:
            return {"error": "El valor inicial no puede ser cero"}
        change = ((new_value - old_value) / old_value) * 100
        return {
            "change_percent": change,
            "formula": "((Nuevo - Antiguo) / Antiguo) × 100",
        }

    @staticmethod
    def discount(original_price: float, discount_percent: float) -> Dict[str, float]:
        """Calculate discount.

        Formula: Discount = Price × (d/100)
        """
        discount_amount = original_price * (discount_percent / 100)
        final_price = original_price - discount_amount
        return {
            "discount_amount": discount_amount,
            "final_price": final_price,
            "formula": "Descuento = Precio × (d/100)",
        }

    @staticmethod
    def rate_conversion(nominal_rate: float, from_frequency: float,
                        to_frequency: float) -> Dict[str, float]:
        """Convert interest rate between compounding frequencies.

        Formula: (1 + r1/n1)^(n1) = (1 + r2/n2)^(n2)
        """
        r1 = nominal_rate / 100
        effective = (1 + r1 / from_frequency) ** from_frequency
        converted = ((effective ** (1 / to_frequency)) - 1) * to_frequency
        return {
            "effective_rate": (effective - 1) * 100,
            "converted_nominal": converted * 100,
            "formula": "(1 + r₁/n₁)^(n₁) = (1 + r₂/n₂)^(n₂)",
        }

    @staticmethod
    def _irr(cashflows: list, tol: float = 1e-6, maxiter: int = 200) -> Optional[float]:
        """Simple IRR via binary search on rate.

        cashflows: list of cash flows where cashflows[0] is initial (usually negative)
        Returns rate as decimal (e.g., 0.12) or None if not converged.
        """
        def npv_at(r):
            total = 0.0
            for i, cf in enumerate(cashflows):
                total += cf / ((1 + r) ** i)
            return total

        low, high = -0.9999, 10.0
        fl, fh = npv_at(low), npv_at(high)
        if fl * fh > 0:
            return None
        for _ in range(maxiter):
            mid = (low + high) / 2
            fm = npv_at(mid)
            if abs(fm) < tol:
                return mid
            if fl * fm < 0:
                high = mid
                fh = fm
            else:
                low = mid
                fl = fm
        return None

    @staticmethod
    def _ddb(cost: float, salvage: float, life: int, period: int) -> float:
        """Compute double-declining-balance depreciation for a specific period.

        period: 1-based period index
        """
        if period < 1 or period > life:
            raise ValueError("period fuera de rango")
        rate = 2.0 / life
        book = cost
        acc = 0.0
        for p in range(1, period + 1):
            dep = book * rate
            # do not depreciate below salvage
            if book - dep < salvage:
                dep = book - salvage
            book -= dep
            acc += dep
            if p == period:
                return dep
        return 0.0
