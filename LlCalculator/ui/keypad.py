"""Dynamic keypad generator."""

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Signal


class KeypadWidget(QWidget):
    """Dynamic keypad that adapts to mode button configurations."""

    button_clicked = Signal(str, str)  # action_type, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setSpacing(6)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._buttons = []

    def set_buttons(self, button_rows: list):
        """Set buttons from mode configuration."""
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons.clear()

        for row_idx, row in enumerate(button_rows):
            col_idx = 0
            for btn_config in row:
                if len(btn_config) == 3:
                    label, btn_type, value = btn_config
                    span = 1
                else:
                    label, btn_type, value, span = btn_config

                btn = QPushButton(label, self)
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                btn.setMinimumHeight(40)

                obj_name = self._get_style_name(btn_type)
                btn.setObjectName(obj_name)
                btn.setToolTip(f"{label}")
                btn.clicked.connect(lambda checked, t=btn_type, v=value: self.button_clicked.emit(t, v))

                self._layout.addWidget(btn, row_idx, col_idx, 1, span)
                self._buttons.append(btn)
                col_idx += span

        for c in range(self._layout.columnCount()):
            self._layout.setColumnStretch(c, 1)

    def _get_style_name(self, btn_type: str) -> str:
        mapping = {
            "num": "numButton",
            "op": "opButton",
            "func": "funcButton",
            "clear": "clearButton",
            "mem": "memButton",
            "eq": "opButton",
            "paren": "funcButton",
            "const": "funcButton",
            "bit": "funcButton",
            "hex": "funcButton",
        }
        return mapping.get(btn_type, "calcButton")
