"""Dialogs for financial function input forms."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt


class FinancialDialog(QDialog):
    """Dialog that shows a small form for common financial functions.

    Usage: instantiate with parent=MainWindow, func_name (string), and mode (FinancialMode instance).
    On accept it will call `mode.evaluate(expr)` and set parent's display.
    """

    def __init__(self, parent, func_name: str, mode):
        super().__init__(parent)
        self.func_name = func_name.lower()
        self.mode = mode
        self.parent = parent
        # Determine language from parent settings (default es)
        self.lang = "es"
        try:
            self.lang = parent.settings.get("language") or "es"
        except Exception:
            pass
        self.trans = self._translations().get(self.lang, self._translations()["es"])
        self.setWindowTitle(f"{func_name} — {self.trans['title']}")
        self.setModal(True)
        self.setMinimumWidth(360)

        self.layout = QVBoxLayout(self)
        self.form = QFormLayout()
        self.inputs = {}

        self._build_form()

        self.layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def _add_field(self, key: str, label: str, placeholder: str = ""):
        le = QLineEdit(self)
        le.setPlaceholderText(placeholder)
        self.form.addRow(label + ":", le)
        self.inputs[key] = le

    def _build_form(self):
        f = self.func_name
        t = self.trans
        if f in ("trmc", "trmci", "trm"):
            self._add_field("pv", t["pv"]) 
            self._add_field("fv", t["fv"]) 
            self._add_field("n", t["n"]) 

        elif f in ("vf", "future_value"):
            self._add_field("pv", t["pv"]) 
            self._add_field("rate", t["rate"]) 
            self._add_field("n", t["n"]) 

        elif f in ("pv", "present_value"):
            self._add_field("fv", t["fv"]) 
            self._add_field("rate", t["rate"]) 
            self._add_field("n", t["n"]) 

        elif f in ("pmt", "annuity"):
            self._add_field("pv", t["pv"]) 
            self._add_field("rate", t["rate"]) 
            self._add_field("n", t["n"]) 

        elif f in ("npv",):
            self._add_field("rate", t["rate"]) 
            self._add_field("cfs", t["cfs"], "-1000;200;300;400")

        elif f in ("irr",):
            self._add_field("cfs", t["cfs"], "-1000;200;300;400")

        elif f in ("ddb", "ddd", "dep_ddb"):
            self._add_field("cost", t["cost"]) 
            self._add_field("salvage", t["salvage"]) 
            self._add_field("life", t["life"]) 
            self._add_field("period", t["period"]) 

        elif f in ("rate_conv",):
            self._add_field("nominal", t["nominal"]) 
            self._add_field("from_freq", t["from_freq"]) 
            self._add_field("to_freq", t["to_freq"]) 

        elif f in ("amort", "loan"):
            self._add_field("principal", t["principal"]) 
            self._add_field("rate", t["rate"]) 
            self._add_field("years", t["years"]) 

        else:
            # fallback: simple input line
            self._add_field("arg", t["args"]) 

        # small hint
        hint = QLabel(self.trans["hint"]) 
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(hint)

    def _on_accept(self):
        f = self.func_name
        try:
            if f in ("npv",):
                rate = float(self.inputs["rate"].text())
                cfs = [float(x.strip()) for x in self.inputs["cfs"].text().split(";") if x.strip()]
                expr = f"npv({rate},{','.join(str(x) for x in cfs)})"

            elif f in ("irr",):
                cfs = [float(x.strip()) for x in self.inputs["cfs"].text().split(";") if x.strip()]
                expr = "irr(" + ",".join(str(x) for x in cfs) + ")"

            else:
                parts = []
                for k, w in self.inputs.items():
                    txt = w.text().strip()
                    if txt == "":
                        raise ValueError("Campo vacío")
                    parts.append(txt)
                expr = f"{self.func_name}({','.join(parts)})"

            res = self.mode.evaluate(expr)
            # show and update main display if available
            QMessageBox.information(self, self.trans["result_title"], str(res))
            try:
                if hasattr(self.parent, "display"):
                    self.parent.display.set_main_text(str(res))
            except Exception:
                pass
            self.accept()
        except Exception as exc:
            QMessageBox.warning(self, self.trans["error_title"], f"{self.trans['invalid_input']}: {exc}")

    def _translations(self):
        return {
            "es": {
                "title": "Calculadora Financiera",
                "pv": "Valor presente (PV)",
                "fv": "Valor futuro (FV)",
                "n": "Periodos (n)",
                "rate": "Tasa anual (%)",
                "cfs": "Flujos de caja (usar ; para separar)",
                "cost": "Costo inicial",
                "salvage": "Valor de salvamento",
                "life": "Vida útil (años)",
                "period": "Periodo (1-based)",
                "nominal": "Tasa nominal (%)",
                "from_freq": "Frecuencia actual (p.ej. 12)",
                "to_freq": "Frecuencia destino (p.ej. 1)",
                "principal": "Principal",
                "years": "Años",
                "args": "Argumentos (coma-separados)",
                "hint": "Rellena los campos y presiona Aceptar. Las cantidades pueden usar punto decimal.",
                "result_title": "Resultado",
                "error_title": "Error",
                "invalid_input": "Entrada inválida",
            },
            "en": {
                "title": "Financial Calculator",
                "pv": "Present Value (PV)",
                "fv": "Future Value (FV)",
                "n": "Periods (n)",
                "rate": "Annual Rate (%)",
                "cfs": "Cash flows (use ; to separate)",
                "cost": "Initial cost",
                "salvage": "Salvage value",
                "life": "Useful life (years)",
                "period": "Period (1-based)",
                "nominal": "Nominal rate (%)",
                "from_freq": "From frequency (e.g. 12)",
                "to_freq": "To frequency (e.g. 1)",
                "principal": "Principal",
                "years": "Years",
                "args": "Arguments (comma-separated)",
                "hint": "Fill fields and press OK. Use dot for decimals.",
                "result_title": "Result",
                "error_title": "Error",
                "invalid_input": "Invalid input",
            }
        }