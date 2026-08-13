"""Main application window."""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QApplication, QMessageBox, QMenuBar, QMenu)
import PySide6.QtCore as QtCore
from PySide6.QtGui import QAction, QKeySequence, QKeyEvent
from PySide6.QtWidgets import QLabel

import core.engine
from modes import BasicMode, AdvancedMode, FinancialMode, ProgrammerMode
import utils.settings
from utils.clipboard import ClipboardManager
from ui.theme_manager import ThemeManager 
from ui.display import CalculatorDisplay
from ui.display import ProgrammerDisplay
from ui.history_panel import HistoryPanel
from ui.keypad import KeypadWidget
from ui.mode_selector import ModeSelector
from ui.preferences import PreferencesDialog
from ui.financial_dialog import FinancialDialog


class MainWindow(QMainWindow):
    """Maximalist calculator main window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MaximalCalc - Calculadora Profesional")
        self.setMinimumSize(900, 650)

        self.settings = utils.settings.AppSettings()
        self.theme_manager = ThemeManager(self)
        self.clipboard = ClipboardManager()
        self.engine = core.engine.CalculatorEngine(
            angle_mode=self.settings.get("angle_mode"),
            precision=self.settings.get("precision"),
        )

        self.modes = {
            "basic": BasicMode(self.engine),
            "advanced": AdvancedMode(self.engine),
            "financial": FinancialMode(self.engine),
            "programmer": ProgrammerMode(self.engine),
        }
        self.current_mode_key = "basic"
        self.current_mode = self.modes["basic"]

        self.expression = ""
        self.last_result = ""
        self.just_evaluated = False

        self._build_ui()
        self._build_menu()
        self._apply_initial_settings()
        self._switch_mode("basic")

    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        left_panel = QWidget(self)
        left_panel.setObjectName("instrumentPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(10)

        self.mode_selector = ModeSelector(self)
        self.mode_selector.group.buttonClicked.connect(self._on_mode_clicked)
        left_layout.addWidget(self.mode_selector)

        self.display = CalculatorDisplay(self)
        self.prog_display = ProgrammerDisplay(self)
        left_layout.addWidget(self.display)
        left_layout.addWidget(self.prog_display)

        self.keypad = KeypadWidget(self)
        self.keypad.button_clicked.connect(self._on_button_clicked)
        left_layout.addWidget(self.keypad, stretch=1)

        self.mem_indicator = QLabel("MEM", self)
        self.mem_indicator.setObjectName("ledIndicator")
        self.mem_indicator.setProperty("active", False)
        left_layout.addWidget(self.mem_indicator, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.history_panel = HistoryPanel(self)
        self.history_panel.entry_selected.connect(self._on_history_selected)
        self.history_panel.history_cleared.connect(self._save_history)

        splitter = QSplitter(QtCore.Qt.Orientation.Horizontal, self)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.history_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)

    def _build_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")
        edit_menu = menubar.addMenu("Editar")
        view_menu = menubar.addMenu("Ver")
        help_menu = menubar.addMenu("Ayuda")

        pref_action = QAction("Preferencias...", self)
        pref_action.setShortcut(QKeySequence("Ctrl+,"))
        pref_action.triggered.connect(self._show_preferences)
        file_menu.addAction(pref_action)

        exit_action = QAction("Salir", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        copy_action = QAction("Copiar resultado", self)
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(self._copy_result)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Pegar", self)
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(self._paste_expression)
        edit_menu.addAction(paste_action)

        dark_action = QAction("Tema Oscuro", self)
        dark_action.triggered.connect(lambda: self._set_theme("dark"))
        view_menu.addAction(dark_action)

        light_action = QAction("Tema Claro", self)
        light_action.triggered.connect(lambda: self._set_theme("light"))
        view_menu.addAction(light_action)

        auto_action = QAction("Tema Automático", self)
        auto_action.triggered.connect(lambda: self._set_theme("auto"))
        view_menu.addAction(auto_action)

        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _apply_initial_settings(self):
        theme = self.settings.get("theme")
        self.theme_manager.apply_theme(theme)
        geometry = self.settings.load_geometry()
        if geometry:
            self.restoreGeometry(geometry)
        self._load_history()

    def _set_theme(self, theme: str):
        self.theme_manager.apply_theme(theme)
        self.settings.set("theme", theme)

    def _on_mode_clicked(self, btn):
        mode = btn.property("mode")
        self._switch_mode(mode)

    def _switch_mode(self, mode_key: str):
        self.current_mode_key = mode_key
        self.current_mode = self.modes[mode_key]
        self.mode_selector.set_mode(mode_key)

        buttons = self.current_mode.get_buttons()
        self.keypad.set_buttons(buttons)

        if mode_key == "programmer":
            self.display.hide()
            self.prog_display.show()
            self._update_programmer_display()
        else:
            self.prog_display.hide()
            self.display.show()
            self.display.set_main_text("0")
            self.display.set_sub_text("")

        self.expression = ""
        self.just_evaluated = False
        self._update_memory_indicator()

    def _on_button_clicked(self, btn_type: str, value: str):
        # If in financial mode, open function-specific dialogs for func buttons
        if self.current_mode_key == "financial" and btn_type == "func":
            dlg = FinancialDialog(self, value, self.current_mode)
            dlg.exec()
            return
        if self.current_mode_key == "programmer":
            self._handle_programmer_button(btn_type, value)
            return

        if btn_type == "num":
            if self.just_evaluated:
                self.expression = ""
                self.just_evaluated = False
            self.expression += value
            self.display.set_main_text(self.expression or "0")

        elif btn_type == "op":
            if self.just_evaluated:
                self.just_evaluated = False
            self.expression += f" {value} "
            self.display.set_main_text(self.expression or "0")

        elif btn_type == "paren":
            if self.just_evaluated:
                self.expression = ""
                self.just_evaluated = False
            self.expression += value
            self.display.set_main_text(self.expression or "0")

        elif btn_type == "func":
            if value in ("neg",):
                return
            if value == "!":
                self.expression += value
            elif value == "^2":
                self.expression += "^2"
            elif value.startswith("10^"):
                self.expression += "10^"
            else:
                self.expression += value
            self.display.set_main_text(self.expression or "0")
            self.just_evaluated = False

        elif btn_type == "const":
            if self.just_evaluated:
                self.expression = ""
                self.just_evaluated = False
            self.expression += value
            self.display.set_main_text(self.expression or "0")

        elif btn_type == "clear":
            if value == "C":
                self.expression = ""
                self.display.set_main_text("0")
                self.display.set_sub_text("")
            elif value == "CE":
                self.expression = ""
                self.display.set_main_text("0")
            elif value == "DEL":
                self.expression = self.expression[:-1].strip()
                self.display.set_main_text(self.expression or "0")

        elif btn_type == "eq":
            self._evaluate()

        elif btn_type == "mem":
            self._handle_memory(value)

    def _evaluate(self):
        if not self.expression:
            return
        expr = self.expression
        result = self.current_mode.evaluate(expr)
        self.last_result = result
        self.display.set_main_text(result)
        self.display.set_sub_text(f"{expr} =")
        self.just_evaluated = True

        if not self.engine.is_error():
            self.history_panel.add_entry(expr, result, self.current_mode.name)
            self._save_history()

    def _handle_memory(self, action: str):
        if action == "MC":
            self.current_mode.memory_clear()
        elif action == "MR":
            val = self.current_mode.memory_recall()
            if self.just_evaluated:
                self.expression = val
                self.just_evaluated = False
            else:
                self.expression += val
            self.display.set_main_text(self.expression or "0")
        elif action == "M+":
            try:
                val = float(self.last_result) if self.last_result else 0
                self.current_mode.memory_add(val)
            except ValueError:
                pass
        elif action == "M-":
            try:
                val = float(self.last_result) if self.last_result else 0
                self.current_mode.memory_subtract(val)
            except ValueError:
                pass
        elif action == "MS":
            try:
                if self.last_result and not self.engine.is_error():
                    self.current_mode.memory_store(float(self.last_result))
            except ValueError:
                pass
        self._update_memory_indicator()

    def _update_memory_indicator(self):
        self.mem_indicator.setProperty("active", self.current_mode.has_memory)
        self.mem_indicator.style().unpolish(self.mem_indicator)
        self.mem_indicator.style().polish(self.mem_indicator)

    def _handle_programmer_button(self, btn_type: str, value: str):
        prog = self.current_mode
        if btn_type == "num":
            prog.input_digit(value)
            self._update_programmer_display()
        elif btn_type == "hex":
            prog.input_digit(value)
            self._update_programmer_display()
        elif btn_type == "bit":
            if value in ("~", "ROL", "ROR"):
                prog.apply_unary(value)
            else:
                prog.prepare_operation(value)
        elif btn_type == "op":
            prog.prepare_operation(value)
        elif btn_type == "eq":
            prog.execute_pending()
            self._update_programmer_display()
        elif btn_type == "clear":
            if value == "C":
                prog.clear()
            elif value == "CE":
                prog.clear_entry()
            elif value == "DEL":
                prog.delete_digit()
            self._update_programmer_display()

    def _update_programmer_display(self):
        values = self.current_mode.get_all_bases()
        self.prog_display.update_values(values)

    def _on_history_selected(self, result: str):
        if self.current_mode_key == "programmer":
            return
        self.expression = result
        self.display.set_main_text(result)
        self.just_evaluated = True

    def _copy_result(self):
        text = self.display.main_text() if self.current_mode_key != "programmer" else self.current_mode.input_buffer
        self.clipboard.copy_text(text)

    def _paste_expression(self):
        text = self.clipboard.paste_text()
        if self.current_mode_key == "programmer":
            text = self.clipboard.sanitize_input(text, "programmer")
            for ch in text:
                if ch in "0123456789ABCDEFabcdef":
                    self.current_mode.input_digit(ch)
            self._update_programmer_display()
        else:
            text = self.clipboard.sanitize_input(text, "math")
            if self.just_evaluated:
                self.expression = text
                self.just_evaluated = False
            else:
                self.expression += text
            self.display.set_main_text(self.expression or "0")

    def _show_preferences(self):
        dlg = PreferencesDialog(self.settings, self)
        if dlg.exec() == PreferencesDialog.DialogCode.Accepted:
            new_settings = dlg.get_settings()
            for k, v in new_settings.items():
                self.settings.set(k, v)
            self.engine.set_precision(new_settings["precision"])
            self.engine.set_angle_mode(new_settings["angle_mode"])
            self.theme_manager.apply_theme(new_settings["theme"])

    def _save_history(self):
        entries = self.history_panel.get_entries()
        self.settings.save_history(entries)

    def _load_history(self):
        pass

    def _show_about(self):
        QMessageBox.about(
            self, "Acerca de MaximalCalc",
            "<h2>MaximalCalc 1.0</h2>"
            "<p>Calculadora de escritorio maximalista multiplataforma.</p>"
            "<p>Python + PySide6. Sin dependencias de red.</p>"
        )

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        modifiers = event.modifiers()

        if modifiers == QtCore.Qt.KeyboardModifier.ControlModifier:
            if key == QtCore.Qt.Key.Key_C:
                self._copy_result()
                return
            elif key == QtCore.Qt.Key.Key_V:
                self._paste_expression()
                return
            super().keyPressEvent(event)
            return

        if self.current_mode_key == "programmer":
            self._handle_programmer_key(key, event.text())
            return

        text = event.text()
        if text in "0123456789":
            self._on_button_clicked("num", text)
        elif text in "+-*/%^":
            self._on_button_clicked("op", text)
        elif text == "(" or text == ")":
            self._on_button_clicked("paren", text)
        elif text == "." or text == ",":
            self._on_button_clicked("num", ".")
        elif key == QtCore.Qt.Key.Key_Return or key == QtCore.Qt.Key.Key_Enter:
            self._on_button_clicked("eq", "=")
        elif key == QtCore.Qt.Key.Key_Backspace:
            self._on_button_clicked("clear", "DEL")
        elif key == QtCore.Qt.Key.Key_Escape:
            self._on_button_clicked("clear", "C")
        elif text.lower() == "e":
            self._on_button_clicked("const", "e")
        elif text == "!":
            self._on_button_clicked("func", "!")
        else:
            super().keyPressEvent(event)

    def _handle_programmer_key(self, key, text):
        if text in "0123456789ABCDEFabcdef":
            self.current_mode.input_digit(text)
            self._update_programmer_display()
        elif key == QtCore.Qt.Key.Key_Backspace:
            self.current_mode.delete_digit()
            self._update_programmer_display()
        elif key == QtCore.Qt.Key.Key_Return or key == QtCore.Qt.Key.Key_Enter:
            self.current_mode.execute_pending()
            self._update_programmer_display()

    def closeEvent(self, event):
        self.settings.save_geometry(self.saveGeometry())
        self._save_history()
        super().closeEvent(event)
