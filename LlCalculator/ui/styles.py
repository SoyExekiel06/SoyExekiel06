"""Maximalist stylesheets for the calculator."""

DARK_STYLESHEET = """
QMainWindow {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a1a2e, stop:1 #16213e);
}

QWidget {
    font-family: "Segoe UI", "Ubuntu", "Helvetica", sans-serif;
}

QFrame#instrumentPanel {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0f0f1a, stop:1 #1a1a2e);
    border: 2px solid #4a4a6a;
    border-radius: 8px;
}

QFrame#displayFrame {
    background-color: #0a0a12;
    border: 2px solid #3a3a5a;
    border-radius: 6px;
    border-bottom: 3px solid #2a2a4a;
    border-right: 3px solid #2a2a4a;
}

QLabel#displayMain {
    color: #00ffaa;
    background-color: transparent;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 32px;
    font-weight: bold;
    padding: 8px;
    qproperty-alignment: AlignRight|AlignVCenter;
}

QLabel#displaySub {
    color: #88ccaa;
    background-color: transparent;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    padding: 4px 8px;
    qproperty-alignment: AlignRight|AlignVCenter;
}

QLabel#baseDisplay {
    color: #aaddff;
    background-color: #0f0f1a;
    border: 1px solid #3a3a5a;
    border-radius: 3px;
    font-family: "Consolas", monospace;
    font-size: 12px;
    padding: 4px;
}

QLabel#ledIndicator {
    color: #333;
    background-color: #1a1a2e;
    border: 1px solid #444;
    border-radius: 8px;
    font-size: 10px;
    padding: 2px 6px;
}

QLabel#ledIndicator[active="true"] {
    color: #00ff00;
    background-color: #003300;
    border: 1px solid #00ff00;
}

QPushButton#modeButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2a2a4a, stop:1 #1f1f3a);
    color: #ccccdd;
    border: 1px solid #4a4a6a;
    border-bottom: 2px solid #151525;
    border-right: 2px solid #151525;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton#modeButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3a3a5a, stop:1 #2f2f4a);
    color: #ffffff;
}

QPushButton#modeButton:checked {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff8c00, stop:1 #cc5500);
    color: #ffffff;
    border: 1px solid #ffaa33;
}

QPushButton#calcButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3a3a5a, stop:1 #2a2a4a);
    color: #eeeeff;
    border: 1px solid #555577;
    border-bottom: 3px solid #1a1a2e;
    border-right: 3px solid #1a1a2e;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    padding: 12px;
    min-width: 48px;
    min-height: 40px;
}

QPushButton#calcButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4a4a6a, stop:1 #3a3a5a);
    border-bottom: 2px solid #1a1a2e;
    border-right: 2px solid #1a1a2e;
}

QPushButton#calcButton:pressed {
    background-color: #22223a;
    border: 1px solid #444466;
    border-bottom: 1px solid #22223a;
    border-right: 1px solid #22223a;
}

QPushButton#numButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4a4a5a, stop:1 #3a3a4a);
    color: #ffffff;
    border: 1px solid #666677;
    border-bottom: 3px solid #22222a;
    border-right: 3px solid #22222a;
    border-radius: 6px;
    font-size: 18px;
    font-weight: bold;
    padding: 12px;
}

QPushButton#numButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5a5a6a, stop:1 #4a4a5a);
}

QPushButton#numButton:pressed {
    background-color: #2a2a3a;
    border: 1px solid #555566;
    border-bottom: 1px solid #2a2a3a;
    border-right: 1px solid #2a2a3a;
}

QPushButton#opButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff8c00, stop:1 #cc5500);
    color: #ffffff;
    border: 1px solid #ffaa33;
    border-bottom: 3px solid #883300;
    border-right: 3px solid #883300;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    padding: 12px;
}

QPushButton#opButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffaa33, stop:1 #dd6600);
}

QPushButton#opButton:pressed {
    background-color: #aa4400;
    border: 1px solid #cc6600;
    border-bottom: 1px solid #aa4400;
    border-right: 1px solid #aa4400;
}

QPushButton#funcButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2a4a6a, stop:1 #1a3a5a);
    color: #aaddff;
    border: 1px solid #4a6a8a;
    border-bottom: 3px solid #0a1a2a;
    border-right: 3px solid #0a1a2a;
    border-radius: 6px;
    font-size: 12px;
    padding: 8px;
}

QPushButton#funcButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3a5a7a, stop:1 #2a4a6a);
}

QPushButton#funcButton:pressed {
    background-color: #152535;
    border: 1px solid #3a5a7a;
    border-bottom: 1px solid #152535;
    border-right: 1px solid #152535;
}

QPushButton#clearButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #cc3333, stop:1 #992222);
    color: #ffffff;
    border: 1px solid #dd5555;
    border-bottom: 3px solid #661111;
    border-right: 3px solid #661111;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
    padding: 10px;
}

QPushButton#clearButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #dd4444, stop:1 #aa3333);
}

QPushButton#clearButton:pressed {
    background-color: #771111;
    border: 1px solid #aa3333;
    border-bottom: 1px solid #771111;
    border-right: 1px solid #771111;
}

QPushButton#memButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4a3a5a, stop:1 #3a2a4a);
    color: #ddbbff;
    border: 1px solid #6a5a7a;
    border-bottom: 3px solid #1a1220;
    border-right: 3px solid #1a1220;
    border-radius: 6px;
    font-size: 11px;
    padding: 6px;
}

QPushButton#memButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5a4a6a, stop:1 #4a3a5a);
}

QListWidget#historyList {
    background-color: #0f0f1a;
    color: #aaccff;
    border: 1px solid #3a3a5a;
    border-radius: 4px;
    font-family: "Consolas", monospace;
    font-size: 13px;
    padding: 4px;
}

QListWidget#historyList::item {
    border-bottom: 1px solid #22223a;
    padding: 4px;
}

QListWidget#historyList::item:selected {
    background-color: #2a4a6a;
    color: #ffffff;
}

QScrollBar:vertical {
    background: #1a1a2e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #4a4a6a;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #5a5a7a;
}

QComboBox, QLineEdit, QSpinBox {
    background-color: #1a1a2e;
    color: #ccccdd;
    border: 1px solid #4a4a6a;
    border-radius: 4px;
    padding: 4px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QDialog {
    background-color: #1a1a2e;
    color: #ccccdd;
}

QLabel {
    color: #ccccdd;
}

QGroupBox {
    color: #ffaa55;
    border: 1px solid #4a4a6a;
    border-radius: 4px;
    margin-top: 8px;
    padding-top: 8px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
"""

LIGHT_STYLESHEET = """
QMainWindow {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e8e8f0, stop:1 #d0d0e0);
}

QWidget {
    font-family: "Segoe UI", "Ubuntu", "Helvetica", sans-serif;
}

QFrame#instrumentPanel {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #dcdce8, stop:1 #c8c8d8);
    border: 2px solid #9999aa;
    border-radius: 8px;
}

QFrame#displayFrame {
    background-color: #f0f0f5;
    border: 2px solid #aaaabb;
    border-radius: 6px;
    border-bottom: 3px solid #888899;
    border-right: 3px solid #888899;
}

QLabel#displayMain {
    color: #006644;
    background-color: transparent;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 32px;
    font-weight: bold;
    padding: 8px;
    qproperty-alignment: AlignRight|AlignVCenter;
}

QLabel#displaySub {
    color: #448866;
    background-color: transparent;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    padding: 4px 8px;
    qproperty-alignment: AlignRight|AlignVCenter;
}

QLabel#baseDisplay {
    color: #224466;
    background-color: #e8e8f0;
    border: 1px solid #aaaabb;
    border-radius: 3px;
    font-family: "Consolas", monospace;
    font-size: 12px;
    padding: 4px;
}

QLabel#ledIndicator {
    color: #888;
    background-color: #e0e0e8;
    border: 1px solid #aaa;
    border-radius: 8px;
    font-size: 10px;
    padding: 2px 6px;
}

QLabel#ledIndicator[active="true"] {
    color: #008800;
    background-color: #ccffcc;
    border: 1px solid #008800;
}

QPushButton#modeButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e0e0f0, stop:1 #c8c8d8);
    color: #444455;
    border: 1px solid #9999aa;
    border-bottom: 2px solid #777788;
    border-right: 2px solid #777788;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton#modeButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f0f0ff, stop:1 #d8d8e8);
    color: #222233;
}

QPushButton#modeButton:checked {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff8c00, stop:1 #cc5500);
    color: #ffffff;
    border: 1px solid #ffaa33;
}

QPushButton#calcButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e8e8f0, stop:1 #d0d0e0);
    color: #333344;
    border: 1px solid #aaaabb;
    border-bottom: 3px solid #888899;
    border-right: 3px solid #888899;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    padding: 12px;
    min-width: 48px;
    min-height: 40px;
}

QPushButton#calcButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f0f0ff, stop:1 #d8d8e8);
    border-bottom: 2px solid #888899;
    border-right: 2px solid #888899;
}

QPushButton#calcButton:pressed {
    background-color: #b8b8c8;
    border: 1px solid #9999aa;
    border-bottom: 1px solid #b8b8c8;
    border-right: 1px solid #b8b8c8;
}

QPushButton#numButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f0f0f5, stop:1 #e0e0e8);
    color: #222233;
    border: 1px solid #bbbbcc;
    border-bottom: 3px solid #9999aa;
    border-right: 3px solid #9999aa;
    border-radius: 6px;
    font-size: 18px;
    font-weight: bold;
    padding: 12px;
}

QPushButton#numButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffffff, stop:1 #f0f0f8);
}

QPushButton#numButton:pressed {
    background-color: #c8c8d8;
    border: 1px solid #aaaabb;
    border-bottom: 1px solid #c8c8d8;
    border-right: 1px solid #c8c8d8;
}

QPushButton#opButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff8c00, stop:1 #cc5500);
    color: #ffffff;
    border: 1px solid #ffaa33;
    border-bottom: 3px solid #883300;
    border-right: 3px solid #883300;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    padding: 12px;
}

QPushButton#opButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ffaa33, stop:1 #dd6600);
}

QPushButton#opButton:pressed {
    background-color: #aa4400;
    border: 1px solid #cc6600;
    border-bottom: 1px solid #aa4400;
    border-right: 1px solid #aa4400;
}

QPushButton#funcButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #d0e0f0, stop:1 #b8c8d8);
    color: #224466;
    border: 1px solid #99aabb;
    border-bottom: 3px solid #778899;
    border-right: 3px solid #778899;
    border-radius: 6px;
    font-size: 12px;
    padding: 8px;
}

QPushButton#funcButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e0f0ff, stop:1 #c8d8e8);
}

QPushButton#funcButton:pressed {
    background-color: #a8b8c8;
    border: 1px solid #8899aa;
    border-bottom: 1px solid #a8b8c8;
    border-right: 1px solid #a8b8c8;
}

QPushButton#clearButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #cc3333, stop:1 #992222);
    color: #ffffff;
    border: 1px solid #dd5555;
    border-bottom: 3px solid #661111;
    border-right: 3px solid #661111;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
    padding: 10px;
}

QPushButton#clearButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #dd4444, stop:1 #aa3333);
}

QPushButton#clearButton:pressed {
    background-color: #771111;
    border: 1px solid #aa3333;
    border-bottom: 1px solid #771111;
    border-right: 1px solid #771111;
}

QPushButton#memButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e0d8f0, stop:1 #c8c0d8);
    color: #553377;
    border: 1px solid #bbaacc;
    border-bottom: 3px solid #9988aa;
    border-right: 3px solid #9988aa;
    border-radius: 6px;
    font-size: 11px;
    padding: 6px;
}

QPushButton#memButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f0e8ff, stop:1 #d8d0e8);
}

QListWidget#historyList {
    background-color: #f0f0f5;
    color: #334466;
    border: 1px solid #aaaabb;
    border-radius: 4px;
    font-family: "Consolas", monospace;
    font-size: 13px;
    padding: 4px;
}

QListWidget#historyList::item {
    border-bottom: 1px solid #d0d0e0;
    padding: 4px;
}

QListWidget#historyList::item:selected {
    background-color: #b8c8d8;
    color: #222233;
}

QScrollBar:vertical {
    background: #e0e0e8;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #9999aa;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #777788;
}

QComboBox, QLineEdit, QSpinBox {
    background-color: #f0f0f5;
    color: #333344;
    border: 1px solid #aaaabb;
    border-radius: 4px;
    padding: 4px;
}

QDialog {
    background-color: #e8e8f0;
    color: #333344;
}

QLabel {
    color: #333344;
}

QGroupBox {
    color: #cc5500;
    border: 1px solid #aaaabb;
    border-radius: 4px;
    margin-top: 8px;
    padding-top: 8px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
"""
