"""Mode selector widget."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup


class ModeSelector(QWidget):
    """Horizontal mode selector with instrument-style buttons."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(4, 4, 4, 4)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.modes = {
            "basic": "Básico",
            "advanced": "Avanzado",
            "financial": "Financiero",
            "programmer": "Programador",
        }

        for key, label in self.modes.items():
            btn = QPushButton(label, self)
            btn.setObjectName("modeButton")
            btn.setCheckable(True)
            btn.setProperty("mode", key)
            self.group.addButton(btn)
            layout.addWidget(btn)

        layout.addStretch()

    def set_mode(self, mode_key: str):
        for btn in self.group.buttons():
            if btn.property("mode") == mode_key:
                btn.setChecked(True)
                break

    def current_mode(self) -> str:
        btn = self.group.checkedButton()
        return btn.property("mode") if btn else "basic"
