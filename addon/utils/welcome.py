# ==================================================================
# addon/In utils/welcome.py
# ==================================================================
# TODO
# - Fix this script and add more comments
# ==================================================================
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QWidget
from aqt.qt import (QDialog, QVBoxLayout, QLabel, QPushButton,
                   QMovie, Qt, QApplication)
from pathlib import Path
from typing import Optional

import os


class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        # Ensure the dialog has its final size before centering
        self.adjustSize()
        self.center_dialog()

    def center_dialog(self):
        """
        Center the dialog on screen or relative to parent
        """
        # Get the screen's geometry
        screen = QApplication.primaryScreen().geometry()

        # Calculate the center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2

        # Ensure we don't go off screen
        x = max(0, min(x, screen.width() - self.width()))
        y = max(0, min(y, screen.height() - self.height()))

        # Move dialog
        self.move(x, y)

    def create_gif_label(self, gif_name: str) -> Optional[QLabel]:
        """Create a QLabel with a GIF movie."""
        try:
            gif_label = QLabel()
            # Fix path joining using Path
            gif_path = str(Path(__file__).parent.parent / "resources" / gif_name)
            if os.path.exists(gif_path):
                movie = QMovie(gif_path)
                gif_label.setMovie(movie)
                movie.start()
                gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                return gif_label
        except Exception:
            return None
        return None

    def setup_ui(self):
        self.setWindowTitle("Welcome to Hanzi2Pinyin!")
        self.setMinimumWidth(800)
        self.setMaximumWidth(1000)
        self.setMinimumHeight(800)
        self.setMaximumHeight(900)

        # Create layout with some padding
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Welcome text
        welcome_label = QLabel(
            "<h2>Welcome to Hanzi2Pinyin!</h2>"
            '<div style="font-size: 16px;">'
            "<p>Thank you for installing Hanzi2Pinyin. This Anki add-on will assist you in creating "
            "pronunciation readings (ruby characters) for Chinese characters using "
            "multiple phonetic systems:</p>"
            "<ul>"
            "<li>Pinyin (拼音)</li>"
            "<li>Zhuyin/Bopomofo (注音/ㄅㄆㄇㄈ)</li>"
            "<li>Jyutping (粵拼) [Planned feature]</li>"
            "<li>Xiao'erjing (小儿经) [Planned feature]</li>"
            "</ul>"
            "</div>"
        )
        welcome_label.setWordWrap(True)
        layout.addWidget(welcome_label)

        # Instructions link
        instructions_label = QLabel(
            '<div style="font-size: 16px;">'
            "<p>For detailed instructions and examples, please visit: "
            "<a href='https://github.com/alyssabedard/Hanzi2Pinyin'>"
            "Quick Start Guide</a></p>"
            "</div>"
        )
        instructions_label.setOpenExternalLinks(True)
        instructions_label.setWordWrap(True)
        layout.addWidget(instructions_label)

        # Tips
        tips_label = QLabel(
            '<div style="font-size: 16px;">'
            "<p><b>Usage:</b></p>"
            "<ul>"
            "<li>Use the ruby button (中[zhōng]) in the editor to add pronunciations</li>"
            "<li>Switch between phonetic systems in Tools → Hanzi2Pinyin → Phonetics</li>"
            "<li>Select text and press the ruby button to add pronunciations</li>"
            "</ul>"
            "</div>"
        )
        tips_label.setWordWrap(True)
        layout.addWidget(tips_label)

        # Create scroll area for GIFs
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # List of GIF filenames
        gifs = ["demo-sentencepinyin.gif", "demo-sentencepinyin-html.gif", "liuqi-jiayou.gif"]

        # Add GIFs to content layout
        for gif_name in gifs:
            gif_label = self.create_gif_label(gif_name)
            if gif_label:
                content_layout.addWidget(gif_label)
                content_layout.addSpacing(10)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        tips_label = QLabel(
            '<p align="center" style="font-size: 40px;"><b>加油！！</b></p>'
        )
        layout.addWidget(tips_label)
        close_button = QPushButton("Get Started")
        # Fix the signal connection
        close_button.clicked.connect(self.accept)  # Changed from close_dialog to accept
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


    def close_dialog(self):
        """
        Handler for the close button click
        """
        self.accept()


def show_welcome_dialog(parent):
    """
    Show the welcome dialog if it's the first launch
    """
    from .config import load_config, mark_first_launch_complete

    config = load_config()
    if config.get('first_launch', True):
        dialog = WelcomeDialog(parent)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.exec()
        mark_first_launch_complete()

