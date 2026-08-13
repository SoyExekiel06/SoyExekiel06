"""Theme management for the calculator."""

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
from .styles import DARK_STYLESHEET, LIGHT_STYLESHEET


class ThemeManager(QObject):
    """Manages application themes and notifies widgets of changes."""

    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_theme = "dark"

    def apply_theme(self, theme_name: str):
        """Apply a theme to the application."""
        self._current_theme = theme_name
        app = QApplication.instance()
        if app is None:
            return

        if theme_name == "dark":
            app.setStyleSheet(DARK_STYLESHEET)
        elif theme_name == "light":
            app.setStyleSheet(LIGHT_STYLESHEET)
        elif theme_name == "auto":
            # Detect system theme (simplified: check palette brightness)
            palette = app.palette()
            bg = palette.color(palette.ColorRole.Window)
            luminance = (0.299 * bg.red() + 0.587 * bg.green() + 0.114 * bg.blue()) / 255
            if luminance < 0.5:
                app.setStyleSheet(DARK_STYLESHEET)
            else:
                app.setStyleSheet(LIGHT_STYLESHEET)
        else:
            app.setStyleSheet(DARK_STYLESHEET)

        self.theme_changed.emit(theme_name)

    def current_theme(self) -> str:
        return self._current_theme
