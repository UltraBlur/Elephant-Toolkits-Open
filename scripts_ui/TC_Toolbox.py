#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elephant VFX Pipeline - Timecode Toolbox (PyQt5 Version)

A professional timecode toolbox combining converter and calculator for VFX workflows.

Features:
    - Timecode Converter: Convert between different timecode formats
    - Timecode Calculator: Add and subtract timecodes
    - Multiple frame rates (23.976 to 60 fps)
    - Auto-formatting of timecode input
    - Dark theme UI matching Elephant VFX Pipeline style

Usage:
    python scripts_ui/TC_Toolbox.py
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
    QComboBox, QScrollArea, QTextEdit, QTabWidget, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPalette, QColor


class TimecodeConverterWidget(QWidget):
    """
    Timecode Converter Widget

    A widget for converting timecode between different formats.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Default settings
        self.current_fps = 25
        self.current_format = 'smpte'
        self.strict_mode = True
        self.drop_frame = False
        self.options_expanded = False

        # Get shared styles from parent
        if isinstance(parent, QTabWidget) and hasattr(parent.parent(), 'common_styles'):
            self.common_styles = parent.parent().common_styles
        else:
            self._init_styles()

        self.setup_ui()

    def _init_styles(self):
        """Initialize common UI styles (fallback if no parent)"""
        self.common_styles = {
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
            'checkbox_style': """
                QCheckBox {
                    color: rgb(145, 145, 145);
                    font-size: 12px;
                    font-family: 'Open Sans', sans-serif;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid rgb(100, 100, 100);
                    border-radius: 3px;
                    background-color: rgb(31, 31, 31);
                }
                QCheckBox::indicator:hover {
                    border: 1px solid rgb(100, 200, 255);
                }
                QCheckBox::indicator:checked {
                    background-color: rgb(100, 200, 255);
                    border: 1px solid rgb(100, 200, 255);
                }
            """
        }

    def setup_ui(self):
        """Setup UI interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # FPS and Format selection
        self.setup_fps_format_selection(main_layout)

        # Advanced options (expandable)
        self.setup_advanced_options(main_layout)
        self.update_strict_mode_availability()
        self.update_drop_frame_availability()

        self.add_separator(main_layout)

        # Input section
        self.setup_input_section(main_layout)
        self.add_separator(main_layout)

        # Convert button
        self.setup_convert_button(main_layout)
        self.add_separator(main_layout)

        # Results section (scrollable)
        self.setup_results_section(main_layout)

        # Add stretch at the bottom
        main_layout.addStretch()

    def setup_fps_format_selection(self, layout):
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

        format_label = QLabel("Input Format")
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
        self.fps_combo.addItems(["23.976", "23.98", "24", "25", "29.97", "30", "48", "50", "59.94", "60", "Custom"])
        self.fps_combo.setCurrentText("25")
        self.fps_combo.setStyleSheet(self.common_styles['combobox_style'])
        self.fps_combo.currentTextChanged.connect(self.on_fps_changed)
        self._add_combobox_arrow(self.fps_combo)
        combo_layout.addWidget(self.fps_combo)

        # Custom FPS input (initially hidden)
        self.custom_fps_input = QLineEdit()
        self.custom_fps_input.setFixedSize(120, 25)
        self.custom_fps_input.setPlaceholderText("Enter FPS")
        self.custom_fps_input.setStyleSheet(self.common_styles['input_style'])
        self.custom_fps_input.setVisible(False)
        self.custom_fps_input.textChanged.connect(self.on_custom_fps_changed)
        self.custom_fps_input.returnPressed.connect(self.apply_custom_fps)
        combo_layout.addWidget(self.custom_fps_input)

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
        self.format_combo.setCurrentIndex(0)
        self.format_combo.setStyleSheet(self.common_styles['combobox_style'])
        self.format_combo.currentIndexChanged.connect(self.on_format_changed)
        self._add_combobox_arrow(self.format_combo, arrow_x=120)
        combo_layout.addWidget(self.format_combo)

        combo_widget = QWidget()
        combo_widget.setLayout(combo_layout)
        layout.addWidget(combo_widget)

    def setup_advanced_options(self, layout):
        """Setup advanced options (collapsible)"""
        # Container for the entire expandable section
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        options_layout.setContentsMargins(0, 5, 0, 0)
        options_layout.setSpacing(5)

        # Toggle button
        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_btn = QPushButton("▶ Advanced Options")
        self.toggle_btn.setFixedHeight(20)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(145, 145, 145);
                border: none;
                text-align: left;
                padding-left: 0px;
                font-size: 11px;
                font-family: 'Open Sans', sans-serif;
            }
            QPushButton:hover {
                color: rgb(100, 200, 255);
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_advanced_options)
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()

        options_layout.addLayout(toggle_layout)

        # Collapsible content
        self.options_content = QWidget()
        self.options_content.setObjectName("options_content")
        self.options_content.setStyleSheet("""
            QWidget#options_content {
                background-color: rgb(35, 35, 40);
                border-radius: 3px;
            }
        """)
        content_layout = QHBoxLayout(self.options_content)
        content_layout.setContentsMargins(10, 8, 10, 8)
        content_layout.setSpacing(15)

        # Strict Mode checkbox
        self.strict_mode_cb = QCheckBox("Strict Mode")
        self.strict_mode_cb.setChecked(True)
        self.strict_mode_cb.setStyleSheet(self.common_styles['checkbox_style'])
        self.strict_mode_cb.stateChanged.connect(self.on_strict_mode_changed)
        content_layout.addWidget(self.strict_mode_cb)

        # Drop Frame checkbox
        self.drop_frame_cb = QCheckBox("Drop Frame")
        self.drop_frame_cb.setStyleSheet(self.common_styles['checkbox_style'])
        self.drop_frame_cb.stateChanged.connect(self.on_drop_frame_changed)
        content_layout.addWidget(self.drop_frame_cb)

        content_layout.addStretch()

        options_layout.addWidget(self.options_content)

        # Initially hide the options
        self.options_content.setMaximumHeight(0)
        self.options_content.setVisible(False)

        layout.addWidget(options_container)

    def toggle_advanced_options(self):
        """Toggle advanced options visibility"""
        self.options_expanded = not self.options_expanded

        if self.options_expanded:
            self.toggle_btn.setText("▼ Advanced Options")
            self.options_content.setMaximumHeight(16777215)
            self.options_content.setVisible(True)
        else:
            self.toggle_btn.setText("▶ Advanced Options")
            self.options_content.setVisible(False)
            self.options_content.setMaximumHeight(0)

    def on_strict_mode_changed(self, state):
        """Handle strict mode checkbox change"""
        self.strict_mode = (state == Qt.Checked)

    def on_drop_frame_changed(self, state):
        """Handle drop frame checkbox change"""
        self.drop_frame = (state == Qt.Checked)

    def update_strict_mode_availability(self):
        """Strict mode is always available for user control"""
        # Strict mode is always enabled for user control, no forced behavior
        self.strict_mode_cb.setEnabled(True)

    def update_drop_frame_availability(self):
        """Enable/disable drop frame based on fps (force enable for 23.98)"""
        fps = self.current_fps
        is_drop_framable = (round(fps, 2) % 29.97 == 0 or round(fps, 2) % 23.98 == 0)

        # Check if fps is 23.98
        is_23_98 = (abs(fps - 23.98) < 0.01)

        if is_23_98:
            # Force enable drop frame for 23.98 and disable checkbox
            self.drop_frame_cb.setChecked(True)
            self.drop_frame_cb.setEnabled(False)
            self.drop_frame = True
        elif is_drop_framable:
            # Enable checkbox for user control
            self.drop_frame_cb.setEnabled(True)
        else:
            # Disable drop frame for non-drop-framable rates
            self.drop_frame_cb.setEnabled(False)
            if self.drop_frame:
                self.drop_frame_cb.setChecked(False)
                self.drop_frame = False

    def setup_input_section(self, layout):
        """Setup input section"""
        input_label = QLabel("Input Timecode")
        input_label.setStyleSheet(self.common_styles['label_style'])
        input_label.setFixedHeight(15)
        layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("00:00:00:00")
        self.input_field.setStyleSheet(self.common_styles['input_style'])
        self.input_field.setFixedHeight(35)
        self.input_field.textChanged.connect(self.format_timecode_input)
        self.input_field.returnPressed.connect(self.convert_timecode)
        layout.addWidget(self.input_field)

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

    def setup_convert_button(self, layout):
        """Setup convert button"""
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setFixedHeight(25)
        self.convert_btn.setStyleSheet(self.common_styles['button_style'])
        self.convert_btn.clicked.connect(self.convert_timecode)
        layout.addWidget(self.convert_btn)

    def setup_results_section(self, layout):
        """Setup results section with all format outputs"""
        results_label = QLabel("Converted Results")
        results_label.setStyleSheet(self.common_styles['label_style'])
        results_label.setFixedHeight(15)
        layout.addWidget(results_label)

        # Create scroll area for results
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: rgb(40, 40, 46);
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: rgb(90, 95, 102);
                min-height: 20px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgb(110, 115, 122);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)

        # Container widget for results
        results_container = QWidget()
        results_layout = QVBoxLayout(results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(8)

        # Dictionary to store result displays
        self.result_displays = {}

        # Define all formats with their display names (common formats first)
        formats = [
            ('frame', 'Frame Count', 'frames'),
            ('time', 'Time', 'seconds'),
            ('smpte', 'SMPTE', 'HH:MM:SS:FF'),
            ('srt', 'SRT', 'HH:MM:SS,mmm'),
            ('dlp', 'DLP', 'HH:MM:SS:sss'),
            ('ffmpeg', 'FFmpeg', 'HH:MM:SS.xx'),
            ('fcpx', 'FCPX', 'fraction/s')
        ]

        for format_key, format_name, format_desc in formats:
            # Format label
            format_label = QLabel(f"{format_name} ({format_desc})")
            format_label.setStyleSheet("color: rgb(145, 145, 145); font-size: 12px; font-family: 'Open Sans', sans-serif;")
            format_label.setFixedHeight(15)
            results_layout.addWidget(format_label)

            # Result display
            result_display = QLineEdit()
            result_display.setReadOnly(True)
            result_display.setPlaceholderText("--")
            result_display.setStyleSheet(self.common_styles['result_style'])
            result_display.setFixedHeight(40)
            result_display.setAlignment(Qt.AlignCenter)
            results_layout.addWidget(result_display)

            # Store reference
            self.result_displays[format_key] = result_display

        results_layout.addStretch()
        scroll_area.setWidget(results_container)
        layout.addWidget(scroll_area)

        # Clear button
        clear_btn = QPushButton("Clear All")
        clear_btn.setFixedHeight(25)
        clear_btn.setStyleSheet(self.common_styles['button_style'])
        clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(clear_btn)

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
        if text == "Custom":
            # Show custom FPS input
            self.custom_fps_input.setVisible(True)
            self.custom_fps_input.setFocus()
            # Keep current FPS until user enters a valid value
        else:
            # Hide custom FPS input
            self.custom_fps_input.setVisible(False)
            try:
                self.current_fps = float(text)
                self.update_strict_mode_availability()
                self.update_drop_frame_availability()
                if self.input_field.text().strip():
                    self.convert_timecode()
            except ValueError:
                self.current_fps = 25

    def on_custom_fps_changed(self, text):
        """Handle custom FPS input change"""
        # Only allow digits and decimal point
        allowed = ''
        has_dot = False
        for c in text:
            if c.isdigit():
                allowed += c
            elif c == '.' and not has_dot:
                allowed += c
                has_dot = True

        if allowed != text:
            # Temporarily disconnect to avoid recursive calls
            self.custom_fps_input.textChanged.disconnect()
            self.custom_fps_input.setText(allowed)
            self.custom_fps_input.textChanged.connect(self.on_custom_fps_changed)
            return

        # Auto-apply custom FPS if valid
        if allowed:
            try:
                fps = float(allowed)
                if fps > 0 and fps <= 1000:  # Reasonable FPS range
                    self.current_fps = fps
                    self.update_strict_mode_availability()
                    self.update_drop_frame_availability()
                    if self.input_field.text().strip():
                        self.convert_timecode()
                    self.status_label.clear()
            except ValueError:
                pass  # Ignore incomplete input like "12."

    def apply_custom_fps(self):
        """Apply custom FPS value (called on Enter key)"""
        text = self.custom_fps_input.text().strip()
        if text:
            try:
                fps = float(text)
                if fps > 0 and fps <= 1000:  # Reasonable FPS range
                    self.current_fps = fps
                    self.update_strict_mode_availability()
                    self.update_drop_frame_availability()
                    if self.input_field.text().strip():
                        self.convert_timecode()
                    self.status_label.clear()
                else:
                    self.show_error("FPS must be between 0 and 1000")
            except ValueError:
                self.show_error("Invalid FPS value")

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
        self.input_field.setPlaceholderText(placeholder)

        self.status_label.clear()

    def format_timecode_input(self):
        """Auto-format timecode input based on selected format"""
        # Temporarily disconnect to avoid recursive calls
        self.input_field.textChanged.disconnect()

        # Get current text and cursor position
        text = self.input_field.text()
        cursor_pos = self.input_field.cursorPosition()

        formatted = text
        new_pos = cursor_pos

        if self.current_format == 'smpte':
            # SMPTE: HH:MM:SS:FF (FF can be 2-4 digits based on FPS)
            # Determine max frame digits based on FPS
            if self.current_fps >= 1000:
                max_frame_digits = 4
                max_total_digits = 10
            elif self.current_fps >= 100:
                max_frame_digits = 3
                max_total_digits = 9
            else:
                max_frame_digits = 2
                max_total_digits = 8

            digits_only = ''.join(filter(str.isdigit, text))
            digits_only = digits_only[:max_total_digits]

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
            # FCPX: fraction/s format
            allowed = ''.join(c for c in text if c.isdigit() or c in ['/', 's'])
            formatted = allowed
            new_pos = min(cursor_pos, len(formatted))

        elif self.current_format == 'frame':
            # Frame: digits only
            digits_only = ''.join(filter(str.isdigit, text))
            formatted = digits_only
            new_pos = min(cursor_pos, len(formatted))

        elif self.current_format == 'time':
            # Time: decimal number
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
        self.input_field.setText(formatted)
        self.input_field.setCursorPosition(min(new_pos, len(formatted)))

        # Reconnect signal
        self.input_field.textChanged.connect(self.format_timecode_input)

    def convert_timecode(self):
        """Convert input timecode to all formats"""
        try:
            # Get input value
            input_text = self.input_field.text().strip()

            if not input_text:
                self.show_error("Please enter a timecode value")
                return

            # Parse timecode with current format
            tc = DfttTimecode(input_text, timecode_type=self.current_format, fps=self.current_fps,
                            drop_frame=self.drop_frame, strict=self.strict_mode)

            # Convert to all formats (in display order)
            self.result_displays['frame'].setText(tc.timecode_output('frame'))
            self.result_displays['time'].setText(tc.timecode_output('time'))
            self.result_displays['smpte'].setText(tc.timecode_output('smpte'))
            self.result_displays['srt'].setText(tc.timecode_output('srt'))
            self.result_displays['dlp'].setText(tc.timecode_output('dlp'))
            self.result_displays['ffmpeg'].setText(tc.timecode_output('ffmpeg'))
            self.result_displays['fcpx'].setText(tc.timecode_output('fcpx'))

            self.status_label.setText("")

        except Exception as e:
            self.show_error(f"Conversion error: {str(e)}")
            self.clear_results()

    def clear_results(self):
        """Clear all result displays"""
        for display in self.result_displays.values():
            display.clear()

    def clear_all(self):
        """Clear input and all results"""
        self.input_field.clear()
        self.clear_results()
        self.status_label.clear()

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


class TimecodeCalculatorWidget(QWidget):
    """
    Timecode Calculator Widget

    A widget for performing arithmetic operations on timecodes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Default settings
        self.current_fps = 25
        self.current_format = 'smpte'
        self.current_operation = '+'
        self.strict_mode = False
        self.drop_frame = False
        self.options_expanded = False

        # Get shared styles from parent
        if isinstance(parent, QTabWidget) and hasattr(parent.parent(), 'common_styles'):
            self.common_styles = parent.parent().common_styles
        else:
            self._init_styles()

        self.setup_ui()

    def _init_styles(self):
        """Initialize common UI styles (fallback if no parent)"""
        self.common_styles = {
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
            """,
            'checkbox_style': """
                QCheckBox {
                    color: rgb(145, 145, 145);
                    font-size: 12px;
                    font-family: 'Open Sans', sans-serif;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid rgb(100, 100, 100);
                    border-radius: 3px;
                    background-color: rgb(31, 31, 31);
                }
                QCheckBox::indicator:hover {
                    border: 1px solid rgb(100, 200, 255);
                }
                QCheckBox::indicator:checked {
                    background-color: rgb(100, 200, 255);
                    border: 1px solid rgb(100, 200, 255);
                }
            """
        }

    def setup_ui(self):
        """Setup UI interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # FPS selection
        self.setup_fps_selection(main_layout)

        # Advanced options (expandable)
        self.setup_advanced_options(main_layout)
        self.update_strict_mode_availability()
        self.update_drop_frame_availability()

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
        self.fps_combo.addItems(["23.976", "23.98", "24", "25", "29.97", "30", "48", "50", "59.94", "60", "Custom"])
        self.fps_combo.setCurrentText("25")
        self.fps_combo.setStyleSheet(self.common_styles['combobox_style'])
        self.fps_combo.currentTextChanged.connect(self.on_fps_changed)
        self._add_combobox_arrow(self.fps_combo)
        combo_layout.addWidget(self.fps_combo)

        # Custom FPS input (initially hidden)
        self.custom_fps_input = QLineEdit()
        self.custom_fps_input.setFixedSize(120, 25)
        self.custom_fps_input.setPlaceholderText("Enter FPS")
        self.custom_fps_input.setStyleSheet(self.common_styles['input_style'])
        self.custom_fps_input.setVisible(False)
        self.custom_fps_input.textChanged.connect(self.on_custom_fps_changed)
        self.custom_fps_input.returnPressed.connect(self.apply_custom_fps)
        combo_layout.addWidget(self.custom_fps_input)

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
        self.format_combo.setCurrentIndex(0)
        self.format_combo.setStyleSheet(self.common_styles['combobox_style'])
        self.format_combo.currentIndexChanged.connect(self.on_format_changed)
        self._add_combobox_arrow(self.format_combo, arrow_x=120)
        combo_layout.addWidget(self.format_combo)

        combo_widget = QWidget()
        combo_widget.setLayout(combo_layout)
        layout.addWidget(combo_widget)

    def setup_advanced_options(self, layout):
        """Setup advanced options (collapsible)"""
        # Container for the entire expandable section
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        options_layout.setContentsMargins(0, 5, 0, 0)
        options_layout.setSpacing(5)

        # Toggle button
        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_btn = QPushButton("▶ Advanced Options")
        self.toggle_btn.setFixedHeight(20)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(145, 145, 145);
                border: none;
                text-align: left;
                padding-left: 0px;
                font-size: 11px;
                font-family: 'Open Sans', sans-serif;
            }
            QPushButton:hover {
                color: rgb(100, 200, 255);
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_advanced_options)
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()

        options_layout.addLayout(toggle_layout)

        # Collapsible content
        self.options_content = QWidget()
        self.options_content.setObjectName("options_content")
        self.options_content.setStyleSheet("""
            QWidget#options_content {
                background-color: rgb(35, 35, 40);
                border-radius: 3px;
            }
        """)
        content_layout = QHBoxLayout(self.options_content)
        content_layout.setContentsMargins(10, 8, 10, 8)
        content_layout.setSpacing(15)

        # Strict Mode checkbox
        self.strict_mode_cb = QCheckBox("Strict Mode")
        self.strict_mode_cb.setChecked(True)
        self.strict_mode_cb.setStyleSheet(self.common_styles['checkbox_style'])
        self.strict_mode_cb.stateChanged.connect(self.on_strict_mode_changed)
        content_layout.addWidget(self.strict_mode_cb)

        # Drop Frame checkbox
        self.drop_frame_cb = QCheckBox("Drop Frame")
        self.drop_frame_cb.setStyleSheet(self.common_styles['checkbox_style'])
        self.drop_frame_cb.stateChanged.connect(self.on_drop_frame_changed)
        content_layout.addWidget(self.drop_frame_cb)

        content_layout.addStretch()

        options_layout.addWidget(self.options_content)

        # Initially hide the options
        self.options_content.setMaximumHeight(0)
        self.options_content.setVisible(False)

        layout.addWidget(options_container)

    def toggle_advanced_options(self):
        """Toggle advanced options visibility"""
        self.options_expanded = not self.options_expanded

        if self.options_expanded:
            self.toggle_btn.setText("▼ Advanced Options")
            self.options_content.setMaximumHeight(16777215)
            self.options_content.setVisible(True)
        else:
            self.toggle_btn.setText("▶ Advanced Options")
            self.options_content.setVisible(False)
            self.options_content.setMaximumHeight(0)

    def on_strict_mode_changed(self, state):
        """Handle strict mode checkbox change"""
        self.strict_mode = (state == Qt.Checked)

    def on_drop_frame_changed(self, state):
        """Handle drop frame checkbox change"""
        self.drop_frame = (state == Qt.Checked)

    def update_strict_mode_availability(self):
        """Strict mode is always available for user control"""
        # Strict mode is always enabled for user control, no forced behavior
        self.strict_mode_cb.setEnabled(True)

    def update_drop_frame_availability(self):
        """Enable/disable drop frame based on fps (force enable for 23.98)"""
        fps = self.current_fps
        is_drop_framable = (round(fps, 2) % 29.97 == 0 or round(fps, 2) % 23.98 == 0)

        # Check if fps is 23.98
        is_23_98 = (abs(fps - 23.98) < 0.01)

        if is_23_98:
            # Force enable drop frame for 23.98 and disable checkbox
            self.drop_frame_cb.setChecked(True)
            self.drop_frame_cb.setEnabled(False)
            self.drop_frame = True
        elif is_drop_framable:
            # Enable checkbox for user control
            self.drop_frame_cb.setEnabled(True)
        else:
            # Disable drop frame for non-drop-framable rates
            self.drop_frame_cb.setEnabled(False)
            if self.drop_frame:
                self.drop_frame_cb.setChecked(False)
                self.drop_frame = False

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
        self.input_a.returnPressed.connect(self.calculate)
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
        self.input_b.returnPressed.connect(self.calculate)
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
        if text == "Custom":
            # Show custom FPS input
            self.custom_fps_input.setVisible(True)
            self.custom_fps_input.setFocus()
            # Keep current FPS until user enters a valid value
        else:
            # Hide custom FPS input
            self.custom_fps_input.setVisible(False)
            try:
                self.current_fps = float(text)
                self.update_strict_mode_availability()
                self.update_drop_frame_availability()
            except ValueError:
                self.current_fps = 25

    def on_custom_fps_changed(self, text):
        """Handle custom FPS input change"""
        # Only allow digits and decimal point
        allowed = ''
        has_dot = False
        for c in text:
            if c.isdigit():
                allowed += c
            elif c == '.' and not has_dot:
                allowed += c
                has_dot = True

        if allowed != text:
            # Temporarily disconnect to avoid recursive calls
            self.custom_fps_input.textChanged.disconnect()
            self.custom_fps_input.setText(allowed)
            self.custom_fps_input.textChanged.connect(self.on_custom_fps_changed)
            return

        # Auto-apply custom FPS if valid
        if allowed:
            try:
                fps = float(allowed)
                if fps > 0 and fps <= 1000:  # Reasonable FPS range
                    self.current_fps = fps
                    self.update_strict_mode_availability()
                    self.update_drop_frame_availability()
                    self.status_label.clear()
            except ValueError:
                pass  # Ignore incomplete input like "12."

    def apply_custom_fps(self):
        """Apply custom FPS value (called on Enter key)"""
        text = self.custom_fps_input.text().strip()
        if text:
            try:
                fps = float(text)
                if fps > 0 and fps <= 1000:  # Reasonable FPS range
                    self.current_fps = fps
                    self.update_strict_mode_availability()
                    self.update_drop_frame_availability()
                    self.status_label.clear()
                else:
                    self.show_error("FPS must be between 0 and 1000")
            except ValueError:
                self.show_error("Invalid FPS value")

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
        """Convert timecode in input field from old format to current format"""
        text = line_edit.text().strip()
        if not text:
            return

        try:
            # Parse timecode with old format
            tc = DfttTimecode(text, timecode_type=old_format, fps=self.current_fps,
                            drop_frame=self.drop_frame, strict=self.strict_mode)

            # Convert to new format
            new_text = tc.timecode_output(self.current_format)

            # Temporarily disconnect signal to avoid triggering formatting
            line_edit.textChanged.disconnect()
            line_edit.setText(new_text)
            line_edit.textChanged.connect(lambda: self.format_timecode_input(line_edit))

        except Exception:
            # If conversion fails, keep original text
            pass

    def convert_result_format(self, old_format):
        """Convert result display from old format to current format"""
        text = self.result_display.text().strip()
        if not text:
            return

        try:
            # Parse timecode with old format
            tc = DfttTimecode(text, timecode_type=old_format, fps=self.current_fps,
                            drop_frame=self.drop_frame, strict=self.strict_mode)

            # Convert to new format
            new_text = tc.timecode_output(self.current_format)
            self.result_display.setText(new_text)

        except Exception:
            # If conversion fails, clear result
            self.result_display.clear()

    def format_timecode_input(self, line_edit):
        """Auto-format timecode input based on selected format"""
        # Temporarily disconnect to avoid recursive calls
        line_edit.textChanged.disconnect()

        # Get current text and cursor position
        text = line_edit.text()
        cursor_pos = line_edit.cursorPosition()

        formatted = text
        new_pos = cursor_pos

        if self.current_format == 'smpte':
            # SMPTE: HH:MM:SS:FF (FF can be 2-4 digits based on FPS)
            # Determine max frame digits based on FPS
            if self.current_fps >= 1000:
                max_frame_digits = 4
                max_total_digits = 10
            elif self.current_fps >= 100:
                max_frame_digits = 3
                max_total_digits = 9
            else:
                max_frame_digits = 2
                max_total_digits = 8

            digits_only = ''.join(filter(str.isdigit, text))
            digits_only = digits_only[:max_total_digits]

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
            # FCPX: fraction/s format
            allowed = ''.join(c for c in text if c.isdigit() or c in ['/', 's'])
            formatted = allowed
            new_pos = min(cursor_pos, len(formatted))

        elif self.current_format == 'frame':
            # Frame: digits only
            digits_only = ''.join(filter(str.isdigit, text))
            formatted = digits_only
            new_pos = min(cursor_pos, len(formatted))

        elif self.current_format == 'time':
            # Time: decimal number
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
            tc_a = DfttTimecode(tc_a_str, timecode_type=self.current_format, fps=self.current_fps,
                              drop_frame=self.drop_frame, strict=self.strict_mode)
            tc_b = DfttTimecode(tc_b_str, timecode_type=self.current_format, fps=self.current_fps,
                              drop_frame=self.drop_frame, strict=self.strict_mode)

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
            format_display = self.format_combo.currentText().split(' ')[0]
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


class TimecodeToolbox(QMainWindow):
    """
    Timecode Toolbox Main Window

    A unified interface combining timecode converter and calculator.
    """

    def __init__(self):
        super().__init__()

        # Define common UI styles
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
            """,
            'checkbox_style': """
                QCheckBox {
                    color: rgb(145, 145, 145);
                    font-size: 12px;
                    font-family: 'Open Sans', sans-serif;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid rgb(100, 100, 100);
                    border-radius: 3px;
                    background-color: rgb(31, 31, 31);
                }
                QCheckBox::indicator:hover {
                    border: 1px solid rgb(100, 200, 255);
                }
                QCheckBox::indicator:checked {
                    background-color: rgb(100, 200, 255);
                    border: 1px solid rgb(100, 200, 255);
                }
            """
        }

    def setup_ui(self):
        """Setup UI interface"""
        # Main window settings
        self.setWindowTitle("🐘 Timecode Toolbox")
        self.setMinimumSize(400, 700)
        self.resize(400, 750)
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

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgb(9, 9, 9);
                background-color: rgb(40, 40, 46);
                border-radius: 3px;
            }
            QTabBar::tab {
                background-color: rgb(31, 31, 31);
                color: rgb(145, 145, 145);
                border: 1px solid rgb(9, 9, 9);
                border-bottom: none;
                padding: 8px 16px;
                margin-right: 2px;
                font-family: 'Open Sans', sans-serif;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: rgb(40, 40, 46);
                color: rgb(255, 255, 255);
                border-bottom: 2px solid rgb(100, 200, 255);
            }
            QTabBar::tab:hover {
                background-color: rgb(53, 53, 58);
            }
        """)

        # Add converter widget
        self.converter_widget = TimecodeConverterWidget(self.tab_widget)
        self.tab_widget.addTab(self.converter_widget, "Converter")

        # Add calculator widget
        self.calculator_widget = TimecodeCalculatorWidget(self.tab_widget)
        self.tab_widget.addTab(self.calculator_widget, "Calculator")

        main_layout.addWidget(self.tab_widget)

    def setup_header(self, layout):
        """Setup header section"""
        title_label = QLabel("Timecode Toolbox")
        title_label.setStyleSheet(
            "color: rgb(255, 255, 255); font-size: 16px; font-weight: regular; font-family: 'Open Sans', sans-serif;"
        )
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        desc_label = QLabel("Convert and calculate timecodes")
        desc_label.setStyleSheet(
            "color: rgb(145, 145, 145); font-size: 11px; font-style: italic; font-family: 'Open Sans', sans-serif;"
        )
        desc_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(desc_label)

    def add_separator(self, layout):
        """Add a separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        separator.setLineWidth(1)
        separator.setStyleSheet("background-color: rgb(9, 9, 9); border: none;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)


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
    window = TimecodeToolbox()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
