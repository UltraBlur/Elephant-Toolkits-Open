#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elephant VFX Pipeline - Timecode Calculator (PyQt5 Version)

A professional timecode calculator for VFX workflows that supports:
- Timecode addition and subtraction using dftt-timecode library
- Multiple frame rates (23.976 to 60 fps)
- Auto-formatting of timecode input (HH:MM:SS:FF)
- Calculation history (last 10 entries)
- Dark theme UI matching vfx_marker_ui.py style

Usage:
    python scripts_ui/TC_Calculator.py
"""

import sys
from pathlib import Path

# Project setup - add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dftt_timecode import DfttTimecode

# PyQt5 imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton, QLineEdit, QFrame,
    QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor


class TimecodeCalculator(QMainWindow):
    """
    Timecode Calculator UI class

    A PyQt5-based calculator for timecode arithmetic operations in VFX workflows.

    Features:
        - Addition and subtraction of timecodes
        - Multi-framerate support (23.976 - 60 fps)
        - Auto-formatting timecode input with colons
        - Calculation history (preserves last 10 calculations)
        - Dark theme matching Elephant VFX Pipeline style

    Attributes:
        current_fps (float): Current frame rate setting
        current_operation (str): Current operation ('+' or '-')
        input_a (QLineEdit): Timecode A input field
        input_b (QLineEdit): Timecode B input field
        result_display (QLineEdit): Result display field
        history_display (QTextEdit): Calculation history display
    """

    def __init__(self):
        super().__init__()

        # Default framerate and timecode format
        self.current_fps = 25
        self.current_format = 'smpte'  # Default to SMPTE format
        self.current_operation = '+'

        # Define common UI styles (matching vfx_marker_ui.py)
        self._init_styles()

        # Setup UI
        self.setup_ui()

    def _init_styles(self):
        """Initialize common UI styles"""
        self.common_styles = {
            'font_family': "'Open Sans', sans-serif",
            'label_style': "color: rgb(145, 145, 145); font-size: 14px; font-weight: semibold; font-family: 'Open Sans', sans-serif;",
            'button_style': """
                QPushButton {
                    background-color: rgb(40, 40, 46);
                    color: rgb(145, 145, 145);
                    border: 1px solid rgb(100, 100, 100);
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: semibold;
                    font-family: 'Open Sans', sans-serif;
                }
                QPushButton:hover {
                    background-color: rgb(53, 53, 58);
                }
                QPushButton:pressed {
                    background-color: rgb(23, 23, 28);
                }
            """,
            'input_style': """
                QLineEdit {
                    background-color: rgb(31, 31, 31);
                    color: rgb(200, 200, 200);
                    border: 1px solid rgb(7, 7, 7);
                    border-radius: 3px;
                    padding: 5px 8px;
                    font-size: 14px;
                    font-family: 'Courier New', 'Monaco', monospace;
                }
                QLineEdit:focus {
                    border: 1px solid rgb(100, 200, 255);
                }
            """,
            'result_style': """
                QLineEdit {
                    background-color: rgb(31, 31, 31);
                    color: rgb(100, 200, 100);
                    border: 1px solid rgb(7, 7, 7);
                    border-radius: 3px;
                    padding: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: 'Courier New', 'Monaco', monospace;
                }
            """,
            'combobox_style': """
                QComboBox {
                    background-color: rgb(31, 31, 31);
                    color: rgb(145, 145, 145);
                    border: 1px solid rgb(7, 7, 7);
                    border-radius: 3px;
                    padding: 3px 8px;
                    font-size: 12px;
                    font-family: 'Open Sans', sans-serif;
                }
                QComboBox::drop-down {
                    border: none;
                    background: transparent;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: rgb(31, 31, 31);
                    color: rgb(145, 145, 145);
                    border: 1px solid rgb(7, 7, 7);
                    selection-background-color: rgb(100, 200, 255);
                }
            """,
            'textedit_style': """
                QTextEdit {
                    background-color: rgb(31, 31, 31);
                    color: rgb(145, 145, 145);
                    border: 1px solid rgb(7, 7, 7);
                    border-radius: 3px;
                    padding: 5px;
                    font-size: 11px;
                    font-family: 'Courier New', 'Monaco', monospace;
                }
            """
        }

    def setup_ui(self):
        """Setup UI interface"""
        # Main window settings
        self.setWindowTitle("🐘 Timecode Calculator")
        self.setMinimumSize(400, 580)
        self.resize(400, 580)
        self.setStyleSheet("background-color: rgb(40, 40, 46);")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Header section
        self.setup_header(main_layout)
        self.add_separator(main_layout)

        # FPS selection
        self.setup_fps_selection(main_layout)
        self.add_separator(main_layout)

        # Input A
        self.setup_input_a(main_layout)

        # Operation selection
        self.setup_operation(main_layout)

        # Input B
        self.setup_input_b(main_layout)

        self.add_separator(main_layout)

        # Calculate button
        self.setup_calculate_button(main_layout)

        # Result display
        self.setup_result(main_layout)

        self.add_separator(main_layout)

        # History
        self.setup_history(main_layout)

        # Add stretch at the bottom
        main_layout.addStretch()

    def setup_header(self, layout):
        """Setup header section"""
        title_label = QLabel("Timecode Calculator")
        title_label.setStyleSheet(
            "color: rgb(255, 255, 255); font-size: 16px; font-weight: regular; font-family: 'Open Sans', sans-serif;"
        )
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

    def setup_fps_selection(self, layout):
        """Setup FPS and Format selection"""
        # Label row
        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(10)

        fps_label = QLabel("Frame Rate")
        fps_label.setStyleSheet(self.common_styles['label_style'])
        fps_label.setFixedHeight(15)
        label_layout.addWidget(fps_label)

        label_layout.addStretch()

        format_label = QLabel("Timecode Format")
        format_label.setStyleSheet(self.common_styles['label_style'])
        format_label.setFixedHeight(15)
        label_layout.addWidget(format_label)

        label_widget = QWidget()
        label_widget.setLayout(label_layout)
        layout.addWidget(label_widget)

        # Combobox row
        combo_layout = QHBoxLayout()
        combo_layout.setContentsMargins(0, 0, 0, 0)
        combo_layout.setSpacing(10)

        self.fps_combo = QComboBox()
        self.fps_combo.setFixedSize(120, 25)
        self.fps_combo.addItems(["23.976", "24", "25", "29.97", "30", "50", "59.94", "60"])
        self.fps_combo.setCurrentText(str(self.current_fps))
        self.fps_combo.setStyleSheet(self.common_styles['combobox_style'])
        self.fps_combo.currentTextChanged.connect(self.on_fps_changed)
        self._add_combobox_arrow(self.fps_combo)
        combo_layout.addWidget(self.fps_combo)

        combo_layout.addStretch()

        self.format_combo = QComboBox()
        self.format_combo.setFixedSize(150, 25)
        self.format_combo.addItems([
            "SMPTE (HH:MM:SS:FF)",
            "SRT (HH:MM:SS,mmm)",
            "DLP (HH:MM:SS:sss)",
            "FFmpeg (HH:MM:SS.xx)",
            "FCPX (fraction/s)",
            "Frame (count)",
            "Time (seconds)"
        ])
        self.format_combo.setCurrentIndex(0)  # Default to SMPTE
        self.format_combo.setStyleSheet(self.common_styles['combobox_style'])
        self.format_combo.currentIndexChanged.connect(self.on_format_changed)
        self._add_combobox_arrow(self.format_combo, arrow_x=120)
        combo_layout.addWidget(self.format_combo)

        combo_widget = QWidget()
        combo_widget.setLayout(combo_layout)
        layout.addWidget(combo_widget)

    def setup_input_a(self, layout):
        """Setup timecode input A"""
        label_a = QLabel("Timecode A")
        label_a.setStyleSheet(self.common_styles['label_style'])
        label_a.setFixedHeight(15)
        layout.addWidget(label_a)

        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("00:00:00:00")
        self.input_a.setStyleSheet(self.common_styles['input_style'])
        self.input_a.setFixedHeight(35)
        self.input_a.textChanged.connect(lambda: self.format_timecode_input(self.input_a))
        self.input_a.returnPressed.connect(self.calculate)  # Enter key to calculate
        layout.addWidget(self.input_a)

    def setup_operation(self, layout):
        """Setup operation selection"""
        op_layout = QHBoxLayout()
        op_layout.setContentsMargins(0, 5, 0, 5)
        op_layout.setSpacing(5)

        self.add_btn = QPushButton("+")
        self.add_btn.setSizePolicy(self.add_btn.sizePolicy().Expanding, self.add_btn.sizePolicy().Fixed)
        self.add_btn.setFixedHeight(25)
        self.add_btn.setStyleSheet(self.get_operation_button_style(True))
        self.add_btn.clicked.connect(lambda: self.set_operation('+'))
        op_layout.addWidget(self.add_btn)

        self.subtract_btn = QPushButton("−")
        self.subtract_btn.setSizePolicy(self.subtract_btn.sizePolicy().Expanding, self.subtract_btn.sizePolicy().Fixed)
        self.subtract_btn.setFixedHeight(25)
        self.subtract_btn.setStyleSheet(self.get_operation_button_style(False))
        self.subtract_btn.clicked.connect(lambda: self.set_operation('-'))
        op_layout.addWidget(self.subtract_btn)

        # Create container widget for buttons
        button_widget = QWidget()
        button_widget.setLayout(op_layout)
        button_widget.setFixedHeight(30)
        layout.addWidget(button_widget)

        # Default operation
        self.current_operation = '+'

    def setup_input_b(self, layout):
        """Setup timecode input B"""
        label_b = QLabel("Timecode B")
        label_b.setStyleSheet(self.common_styles['label_style'])
        label_b.setFixedHeight(15)
        layout.addWidget(label_b)

        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("00:00:00:00")
        self.input_b.setStyleSheet(self.common_styles['input_style'])
        self.input_b.setFixedHeight(35)
        self.input_b.textChanged.connect(lambda: self.format_timecode_input(self.input_b))
        self.input_b.returnPressed.connect(self.calculate)  # Enter key to calculate
        layout.addWidget(self.input_b)

    def setup_calculate_button(self, layout):
        """Setup calculate button"""
        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.setFixedHeight(25)
        self.calc_btn.setStyleSheet(self.common_styles['button_style'])
        self.calc_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calc_btn)

    def setup_result(self, layout):
        """Setup result display"""
        result_label = QLabel("Result")
        result_label.setStyleSheet(self.common_styles['label_style'])
        result_label.setFixedHeight(15)
        layout.addWidget(result_label)

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("00:00:00:00")
        self.result_display.setStyleSheet(self.common_styles['result_style'])
        self.result_display.setFixedHeight(40)
        self.result_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_display)

        # Status label for errors
        self.status_label = QLabel("")
        self.status_label.setFixedHeight(20)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgb(200, 100, 100);
                font-size: 11px;
                font-style: italic;
            }
        """)
        layout.addWidget(self.status_label)

    def setup_history(self, layout):
        """Setup calculation history"""
        history_label = QLabel("History")
        history_label.setStyleSheet(self.common_styles['label_style'])
        history_label.setFixedHeight(15)
        layout.addWidget(history_label)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setFixedHeight(120)
        self.history_display.setStyleSheet(self.common_styles['textedit_style'])
        layout.addWidget(self.history_display)

        # Clear history button
        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.setFixedHeight(25)
        clear_history_btn.setStyleSheet(self.common_styles['button_style'])
        clear_history_btn.clicked.connect(self.clear_history)
        layout.addWidget(clear_history_btn)

    def get_operation_button_style(self, is_selected):
        """Get style for operation button"""
        if is_selected:
            return """
                QPushButton {
                    background-color: rgb(100, 200, 255);
                    color: rgb(255, 255, 255);
                    border: 2px solid rgb(255, 255, 255);
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: semibold;
                    font-family: 'Open Sans', sans-serif;
                }
                QPushButton:hover {
                    background-color: rgb(120, 210, 255);
                }
            """
        else:
            return """
                QPushButton {
                    background-color: rgb(40, 40, 46);
                    color: rgb(145, 145, 145);
                    border: 1px solid rgb(100, 100, 100);
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: semibold;
                    font-family: 'Open Sans', sans-serif;
                }
                QPushButton:hover {
                    background-color: rgb(53, 53, 58);
                }
            """

    def add_separator(self, layout):
        """Add a separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        separator.setLineWidth(1)
        separator.setStyleSheet("background-color: rgb(9, 9, 9); border: none;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

    def _add_combobox_arrow(self, combobox, arrow_x=90):
        """Add custom arrow to combobox"""
        arrow_label = QLabel("⌄", combobox)
        arrow_label.setStyleSheet("""
            QLabel {
                color: rgb(145, 145, 145);
                background: transparent;
                font-size: 10px;
                border: none;
            }
        """)
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setGeometry(arrow_x, 4, 15, 12)
        arrow_label.setAttribute(Qt.WA_TransparentForMouseEvents)

    # Event handlers
    def on_fps_changed(self, text):
        """Handle FPS change"""
        try:
            self.current_fps = float(text)
        except ValueError:
            self.current_fps = 25

    def on_format_changed(self, index):
        """Handle format change"""
        format_map = {
            0: 'smpte',
            1: 'srt',
            2: 'dlp',
            3: 'ffmpeg',
            4: 'fcpx',
            5: 'frame',
            6: 'time'
        }
        old_format = self.current_format
        self.current_format = format_map.get(index, 'smpte')

        # Update placeholder text based on format
        placeholder_map = {
            'smpte': '00:00:00:00',
            'srt': '00:00:00,000',
            'dlp': '00:00:00:000',
            'ffmpeg': '00:00:00.00',
            'fcpx': '0/1s',
            'frame': '0',
            'time': '0.0'
        }
        placeholder = placeholder_map.get(self.current_format, '00:00:00:00')
        self.input_a.setPlaceholderText(placeholder)
        self.input_b.setPlaceholderText(placeholder)
        self.result_display.setPlaceholderText(placeholder)

        # Convert existing timecodes to new format instead of clearing
        self.convert_input_format(self.input_a, old_format)
        self.convert_input_format(self.input_b, old_format)
        self.convert_result_format(old_format)

        self.status_label.clear()

    def convert_input_format(self, line_edit, old_format):
        """
        Convert timecode in input field from old format to current format

        Args:
            line_edit (QLineEdit): The input field to convert
            old_format (str): The previous timecode format
        """
        text = line_edit.text().strip()
        if not text:
            return

        try:
            # Parse timecode with old format
            tc = DfttTimecode(text, timecode_type=old_format, fps=self.current_fps)

            # Convert to new format
            new_text = tc.timecode_output(self.current_format)

            # Temporarily disconnect signal to avoid triggering formatting
            line_edit.textChanged.disconnect()
            line_edit.setText(new_text)
            line_edit.textChanged.connect(lambda: self.format_timecode_input(line_edit))

        except Exception as e:
            # If conversion fails, keep original text
            pass

    def convert_result_format(self, old_format):
        """
        Convert result display from old format to current format

        Args:
            old_format (str): The previous timecode format
        """
        text = self.result_display.text().strip()
        if not text:
            return

        try:
            # Parse timecode with old format
            tc = DfttTimecode(text, timecode_type=old_format, fps=self.current_fps)

            # Convert to new format
            new_text = tc.timecode_output(self.current_format)
            self.result_display.setText(new_text)

        except Exception as e:
            # If conversion fails, clear result
            self.result_display.clear()

    def format_timecode_input(self, line_edit):
        """
        Auto-format timecode input based on selected format

        Automatically formats user input according to the current timecode format.
        Supports multiple formats with intelligent separators and digit limits.

        Args:
            line_edit (QLineEdit): The input field to format

        Formats:
            SMPTE: HH:MM:SS:FF (8 digits, colons)
            SRT: HH:MM:SS,mmm (9 digits, colons + comma)
            DLP: HH:MM:SS:sss (9 digits, colons)
            FFmpeg: HH:MM:SS.xx (8 digits, colons + dot)
            FCPX: fraction/s (allow digits and '/')
            Frame: digit only (no formatting)
            Time: decimal number (allow digits and '.')
        """
        # Temporarily disconnect to avoid recursive calls
        line_edit.textChanged.disconnect()

        # Get current text and cursor position
        text = line_edit.text()
        cursor_pos = line_edit.cursorPosition()

        formatted = text
        new_pos = cursor_pos

        if self.current_format == 'smpte':
            # SMPTE: HH:MM:SS:FF or HH:MM:SS;FF
            digits_only = ''.join(filter(str.isdigit, text))
            digits_only = digits_only[:8]

            formatted = ''
            for i, digit in enumerate(digits_only):
                formatted += digit
                if i in [1, 3, 5] and i < len(digits_only) - 1:
                    formatted += ':'

            digits_before = len(''.join(filter(str.isdigit, text[:cursor_pos])))
            new_pos = digits_before
            if digits_before > 2:
                new_pos += 1
            if digits_before > 4:
                new_pos += 1
            if digits_before > 6:
                new_pos += 1

        elif self.current_format == 'srt':
            # SRT: HH:MM:SS,mmm
            digits_only = ''.join(filter(str.isdigit, text))
            digits_only = digits_only[:9]

            formatted = ''
            for i, digit in enumerate(digits_only):
                formatted += digit
                if i == 1 or i == 3:
                    formatted += ':'
                elif i == 5 and i < len(digits_only) - 1:
                    formatted += ','

            digits_before = len(''.join(filter(str.isdigit, text[:cursor_pos])))
            new_pos = digits_before
            if digits_before > 2:
                new_pos += 1
            if digits_before > 4:
                new_pos += 1
            if digits_before > 6:
                new_pos += 1

        elif self.current_format == 'dlp':
            # DLP: HH:MM:SS:sss
            digits_only = ''.join(filter(str.isdigit, text))
            digits_only = digits_only[:9]

            formatted = ''
            for i, digit in enumerate(digits_only):
                formatted += digit
                if i in [1, 3, 5] and i < len(digits_only) - 1:
                    formatted += ':'

            digits_before = len(''.join(filter(str.isdigit, text[:cursor_pos])))
            new_pos = digits_before
            if digits_before > 2:
                new_pos += 1
            if digits_before > 4:
                new_pos += 1
            if digits_before > 6:
                new_pos += 1

        elif self.current_format == 'ffmpeg':
            # FFmpeg: HH:MM:SS.xx
            digits_only = ''.join(filter(str.isdigit, text))
            digits_only = digits_only[:8]

            formatted = ''
            for i, digit in enumerate(digits_only):
                formatted += digit
                if i == 1 or i == 3:
                    formatted += ':'
                elif i == 5 and i < len(digits_only) - 1:
                    formatted += '.'

            digits_before = len(''.join(filter(str.isdigit, text[:cursor_pos])))
            new_pos = digits_before
            if digits_before > 2:
                new_pos += 1
            if digits_before > 4:
                new_pos += 1
            if digits_before > 6:
                new_pos += 1

        elif self.current_format == 'fcpx':
            # FCPX: fraction/s format (e.g., "1001/30s")
            # Allow digits, '/', and 's'
            allowed = ''.join(c for c in text if c.isdigit() or c in ['/', 's'])
            formatted = allowed
            new_pos = min(cursor_pos, len(formatted))

        elif self.current_format == 'frame':
            # Frame: digits only, no separators
            digits_only = ''.join(filter(str.isdigit, text))
            formatted = digits_only
            new_pos = min(cursor_pos, len(formatted))

        elif self.current_format == 'time':
            # Time: decimal number (digits and one dot)
            # Allow negative sign at start
            allowed = ''
            has_dot = False
            for i, c in enumerate(text):
                if c.isdigit():
                    allowed += c
                elif c == '.' and not has_dot:
                    allowed += c
                    has_dot = True
                elif c == '-' and i == 0:
                    allowed += c
            formatted = allowed
            new_pos = min(cursor_pos, len(formatted))

        # Set formatted text and cursor position
        line_edit.setText(formatted)
        line_edit.setCursorPosition(min(new_pos, len(formatted)))

        # Reconnect signal
        line_edit.textChanged.connect(lambda: self.format_timecode_input(line_edit))

    def set_operation(self, op):
        """Set current operation"""
        self.current_operation = op

        # Update button styles
        if op == '+':
            self.add_btn.setStyleSheet(self.get_operation_button_style(True))
            self.subtract_btn.setStyleSheet(self.get_operation_button_style(False))
        else:
            self.add_btn.setStyleSheet(self.get_operation_button_style(False))
            self.subtract_btn.setStyleSheet(self.get_operation_button_style(True))

    def calculate(self):
        """Perform timecode calculation"""
        try:
            # Get input values
            tc_a_str = self.input_a.text().strip()
            tc_b_str = self.input_b.text().strip()

            if not tc_a_str or not tc_b_str:
                self.show_error("Please enter both timecode values")
                return

            # Parse timecodes with current format
            tc_a = DfttTimecode(tc_a_str, timecode_type=self.current_format, fps=self.current_fps)
            tc_b = DfttTimecode(tc_b_str, timecode_type=self.current_format, fps=self.current_fps)

            # Perform calculation
            if self.current_operation == '+':
                result = tc_a + tc_b
                op_symbol = '+'
            else:
                result = tc_a - tc_b
                op_symbol = '−'

            # Display result in selected format
            result_str = result.timecode_output(self.current_format)
            self.result_display.setText(result_str)
            self.status_label.setText("")

            # Add to history
            tc_a_str_formatted = tc_a.timecode_output(self.current_format)
            tc_b_str_formatted = tc_b.timecode_output(self.current_format)
            format_display = self.format_combo.currentText().split(' ')[0]  # Get format name only
            history_entry = f"{tc_a_str_formatted} {op_symbol} {tc_b_str_formatted} = {result_str} [{format_display} @ {self.current_fps}fps]"
            self.add_to_history(history_entry)

        except Exception as e:
            self.show_error(f"Calculation error: {str(e)}")

    def add_to_history(self, entry):
        """Add entry to history"""
        current_history = self.history_display.toPlainText()
        if current_history:
            new_history = entry + "\n" + current_history
        else:
            new_history = entry

        # Keep only last 10 entries
        lines = new_history.split('\n')
        if len(lines) > 10:
            lines = lines[:10]

        self.history_display.setPlainText('\n'.join(lines))

    def clear_history(self):
        """Clear calculation history"""
        self.history_display.clear()

    def show_error(self, message):
        """Show error message"""
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgb(200, 100, 100);
                font-size: 11px;
                font-style: italic;
            }
        """)
        self.status_label.setText(message)

    def show_success(self, message):
        """Show success message"""
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgb(100, 200, 100);
                font-size: 11px;
                font-style: italic;
            }
        """)
        self.status_label.setText(message)

        # Auto clear after 2 seconds
        QTimer.singleShot(2000, lambda: self.status_label.setText(""))


def main():
    """Main function"""
    import os

    # Suppress macOS input method warnings
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(40, 40, 46))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(31, 31, 31))
    palette.setColor(QPalette.AlternateBase, QColor(40, 40, 46))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(40, 40, 46))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(100, 200, 255))
    palette.setColor(QPalette.Highlight, QColor(100, 200, 255))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

    # Create and show main window
    window = TimecodeCalculator()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
