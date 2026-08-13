"""Application settings persistence using QSettings."""

from PySide6.QtCore import QSettings
from .config import DEFAULT_CONFIG


class AppSettings:
    """Manages application settings persistence."""

    def __init__(self):
        self._settings = QSettings("MaximalCalc", "Calculator")

    def get(self, key: str):
        """Get a setting value, falling back to defaults."""
        default = DEFAULT_CONFIG.get(key)
        value = self._settings.value(key, default)
        # QSettings may return strings for numbers
        if key == "precision" and value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        return value if value is not None else default

    def set(self, key: str, value):
        """Set a setting value."""
        self._settings.setValue(key, value)

    def save_geometry(self, geometry):
        self._settings.setValue("window_geometry", geometry)

    def load_geometry(self):
        return self._settings.value("window_geometry")

    def save_history(self, history_list):
        """Save history as a list of strings."""
        self._settings.setValue("history", history_list)

    def load_history(self):
        """Load history as a list of strings."""
        data = self._settings.value("history", [])
        if isinstance(data, str):
            return []
        return data if data else []
