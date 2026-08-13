"""Preferences dialog."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QGroupBox, QFormLayout
)


class PreferencesDialog(QDialog):
    """Application preferences dialog."""

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Preferencias")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)

        appearance_group = QGroupBox("Apariencia", self)
        form = QFormLayout(appearance_group)

        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(["Oscuro", "Claro", "Automático"])
        self.theme_combo.setCurrentText(self._theme_to_label(self.settings.get("theme")))
        form.addRow("Tema:", self.theme_combo)

        self.lang_combo = QComboBox(self)
        self.lang_combo.addItems(["Español", "English"])
        current_lang = self.settings.get("language")
        self.lang_combo.setCurrentText("Español" if current_lang == "es" else "English")
        form.addRow("Idioma:", self.lang_combo)

        layout.addWidget(appearance_group)

        precision_group = QGroupBox("Precisión", self)
        pform = QFormLayout(precision_group)

        self.precision_combo = QComboBox(self)
        self.precision_combo.addItems(["Automático", "2", "4", "6", "10", "15"])
        current_prec = self.settings.get("precision")
        prec_text = "Automático" if current_prec == -1 else str(current_prec)
        self.precision_combo.setCurrentText(prec_text)
        pform.addRow("Decimales:", self.precision_combo)

        layout.addWidget(precision_group)

        angle_group = QGroupBox("Ángulos", self)
        aform = QFormLayout(angle_group)

        self.angle_combo = QComboBox(self)
        self.angle_combo.addItems(["Grados", "Radianes", "Gradianes"])
        self.angle_combo.setCurrentText(self._angle_to_label(self.settings.get("angle_mode")))
        aform.addRow("Unidad:", self.angle_combo)

        layout.addWidget(angle_group)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar", self)
        self.save_btn.setObjectName("opButton")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancelar", self)
        self.cancel_btn.setObjectName("calcButton")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def get_settings(self) -> dict:
        theme_map = {"Oscuro": "dark", "Claro": "light", "Automático": "auto"}
        angle_map = {"Grados": "degrees", "Radianes": "radians", "Gradianes": "gradians"}
        prec_text = self.precision_combo.currentText()
        precision = -1 if prec_text == "Automático" else int(prec_text)
        lang_map = {"Español": "es", "English": "en"}
        return {
            "theme": theme_map[self.theme_combo.currentText()],
            "precision": precision,
            "angle_mode": angle_map[self.angle_combo.currentText()],
            "language": lang_map[self.lang_combo.currentText()],
        }

    def _theme_to_label(self, theme: str) -> str:
        return {"dark": "Oscuro", "light": "Claro", "auto": "Automático"}.get(theme, "Oscuro")

    def _angle_to_label(self, angle: str) -> str:
        return {"degrees": "Grados", "radians": "Radianes", "gradians": "Gradianes"}.get(angle, "Grados")
