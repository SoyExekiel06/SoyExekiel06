"""Clipboard utilities."""

from PySide6.QtWidgets import QApplication


class ClipboardManager:
    """Manages clipboard operations."""

    @staticmethod
    def copy_text(text: str):
        """Copy text to system clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    @staticmethod
    def paste_text() -> str:
        """Paste text from system clipboard."""
        clipboard = QApplication.clipboard()
        return clipboard.text()

    @staticmethod
    def sanitize_input(text: str, mode: str = "math") -> str:
        """Sanitize pasted text for calculator input.

        Removes characters that are not valid for the given mode.
        """
        if mode == "math":
            allowed = set("0123456789.+-*/%^!()eE ")
            allowed.update("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_",)
            allowed.update(",")
            return "".join(ch for ch in text if ch in allowed)
        elif mode == "programmer":
            allowed = set("0123456789ABCDEFabcdef+-*/%^!&|~<>()")
            return "".join(ch for ch in text if ch in allowed)
        return text
