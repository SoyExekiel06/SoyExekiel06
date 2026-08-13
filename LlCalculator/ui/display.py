"""Calculator display widgets."""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class CalculatorDisplay(QFrame):
    """Main display widget with primary and secondary readouts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("displayFrame")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(8, 8, 8, 8)

        self.sub_display = QLabel("", self)
        self.sub_display.setObjectName("displaySub")
        self.sub_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.sub_display)

        self.main_display = QLabel("0", self)
        self.main_display.setObjectName("displayMain")
        self.main_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.main_display)

    def set_main_text(self, text: str):
        self.main_display.setText(text)

    def set_sub_text(self, text: str):
        self.sub_display.setText(text)

    def main_text(self) -> str:
        return self.main_display.text()

    def sub_text(self) -> str:
        return self.sub_display.text()


class ProgrammerDisplay(QFrame):
    """Display for programmer mode showing all bases."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("displayFrame")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 8, 8, 8)

        self.dec_label = self._create_base_label("DEC")
        self.hex_label = self._create_base_label("HEX")
        self.oct_label = self._create_base_label("OCT")
        self.bin_label = self._create_base_label("BIN")

        layout.addWidget(self.dec_label)
        layout.addWidget(self.hex_label)
        layout.addWidget(self.oct_label)
        layout.addWidget(self.bin_label)

    def _create_base_label(self, prefix: str) -> QLabel:
        label = QLabel(f"{prefix}: 0", self)
        label.setObjectName("baseDisplay")
        return label

    def update_values(self, values: dict):
        self.dec_label.setText(f"DEC: {values.get('DEC', '0')}")
        self.hex_label.setText(f"HEX: {values.get('HEX', '0')}")
        self.oct_label.setText(f"OCT: {values.get('OCT', '0')}")
        self.bin_label.setText(f"BIN: {values.get('BIN', '0')}")
