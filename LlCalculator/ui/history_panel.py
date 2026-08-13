"""History panel widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Signal


class HistoryPanel(QWidget):
    """Panel showing calculation history."""

    entry_selected = Signal(str)
    history_cleared = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("historyList")
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Limpiar", self)
        self.clear_btn.setObjectName("calcButton")
        self.clear_btn.setToolTip("Eliminar todo el historial")
        self.clear_btn.clicked.connect(self._clear_history)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)

        self._entries = []

    def add_entry(self, expression: str, result: str, mode_name: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f"[{timestamp}] [{mode_name}]\n  {expression} = {result}"
        self.list_widget.addItem(text)
        self._entries.append((expression, result))
        self.list_widget.scrollToBottom()

    def _on_item_clicked(self, item):
        text = item.text()
        if "= " in text:
            result = text.split("= ")[-1]
            self.entry_selected.emit(result)

    def _clear_history(self):
        reply = QMessageBox.question(
            self, "Confirmar", "¿Borrar todo el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.list_widget.clear()
            self._entries.clear()
            self.history_cleared.emit()

    def get_entries(self) -> list:
        return self._entries.copy()
