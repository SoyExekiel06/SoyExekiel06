#!/usr/bin/env python3
"""Entry point for MaximalCalc."""

import sys
import PySide6.QtWidgets as QTwidgets
from PySide6.QtCore import Qt
import ui.main_window as mainwindow

def main():
    # Try to set a sensible High DPI rounding policy when available.
    try:
        QTwidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except Exception:
        # Not all PySide6/Qt builds expose this API; continue gracefully.
        pass

    app = QTwidgets.QApplication(sys.argv)
    app.setApplicationName("MaximalCalc")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("MaximalCalc")

    window = mainwindow.MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
