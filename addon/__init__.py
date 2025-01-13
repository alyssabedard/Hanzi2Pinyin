# ==================================================================
# Hanzi2Pinyin - Anki Add-on
# ==================================================================
#  Main add-on entry point
#   - Anki loads the add-on by executing __init__.py directly
# ==================================================================
# Author: Alyssa Bédard
# License: MIT License
# GitHub: https://github.com/alyssabedard/Hanzi2Pinyin
#
# Anki addon that automatically converts Chinese characters (Hanzi)
# to ruby-annotated text with pinyin and zhuyin readings.
#
# Copyright (c) 2025 Alyssa Bédard
# ==================================================================

DEBUG = True  # Set to False in production


import sys
from pathlib import Path

# Return absolute path to the directory
# containing the current Python script file
addon_path = Path(__file__).parent
if str(addon_path) not in sys.path:
    sys.path.append(str(addon_path))

# Uncomment to check if the file is being loaded
# showInfo("Addon is loading!")

from .components.ruby_button import setup_editor_ruby_button
from .utils import display_unimplemented_message, display_about_dialog, update_pronunciation_type, load_config, show_welcome_dialog

mw = None


# ==================================================================
# Utils and Helper methods
# ==================================================================

def get_display_about_dialog() -> None:
    display_about_dialog()


def get_unimplemented_message() -> None:
    display_unimplemented_message()


def open_github():
    from aqt.qt import QUrl, QDesktopServices
    QDesktopServices.openUrl(QUrl("https://github.com/alyssabedard/Hanzi2Pinyin/issues"))


def on_pinyin_changed(pinyin_action, zhuyin_action):
    if pinyin_action.isChecked():
        zhuyin_action.setChecked(False)
        update_pronunciation_type('pinyin')
    else:
        zhuyin_action.setChecked(True)
        update_pronunciation_type('zhuyin')

def on_zhuyin_changed(pinyin_action, zhuyin_action):
    if zhuyin_action.isChecked():
        pinyin_action.setChecked(False)
        update_pronunciation_type('zhuyin')
    else:
        pinyin_action.setChecked(True)
        update_pronunciation_type('pinyin')

# ==================================================================
# Main method
# ==================================================================

def init_addon():
    """
    Initialize the addon's menu items and buttons in Anki's interface.
    This function creates a submenu under Anki's Tools menu with options for:
    - Phonetics
    - Help

    The _init_ script separates Anki-specific code from the core functionality,
    in order to:
    1. Run normally within Anki
    2. Be tested independently without Anki dependencies

    Note: ImportError handling allows running tests without Anki,
    as test environments won't have access to Anki's GUI components.
    """
    try:
        from aqt import mw

        if mw is None:
            return  # Exit early if no Anki window

        # Check version compatibility before initializing
        from .utils.versions import check_anki_version
        if not check_anki_version():
            return

        from aqt.qt import QMenu, QAction
        from aqt.utils import qconnect, showInfo

        # Show welcome dialog
        show_welcome_dialog(mw)

        # Load config at startup
        config = load_config()

        # ==================================================================
        # Submenu in Anki's toolbar menu
        # ==================================================================

        submenu = QMenu("Hanzi2Pinyin", mw)
        mw.form.menuTools.addMenu(submenu)

        # ------------------------------------------------------------------
        # Add-on SUBMENU Tools/Hanzi2Pinyin
        #   Tools Menu
        #    └── Hanzi2Pinyin             # Hanzi2Pinyin submenu
        #        ├── Phonetics          # QAction
        #        ├── Help               # QAction
        # ------------------------------------------------------------------
        # - Each QAction is connected to a function using qconnect
        # - Qt methods used by Anki to connect signals to slots (event handlers):
        #       qconnect(some_action.triggered, do_something)
        #           some_action         is a signal
        #           do_something        is the function that will be called
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        #                           Phonetic
        # ------------------------------------------------------------------
        # Add actions for submenu
        phonetic_menu = QMenu("Phonetics", mw)
        submenu.addMenu(phonetic_menu)

        # Create actions with "check-able" property
        pinyin_action = QAction("Pinyin", mw)
        pinyin_action.setCheckable(True)
        zhuyin_action = QAction("Zhuyin/Bopomofo", mw)
        zhuyin_action.setCheckable(True)

        # Set initial state based on saved config
        pinyin_action.setChecked(config['pronunciation_type'] == 'pinyin')
        zhuyin_action.setChecked(config['pronunciation_type'] == 'zhuyin')


        phonetic_menu.addAction(pinyin_action)
        phonetic_menu.addAction(zhuyin_action)

        # Connect actions to their respective functions
        # Connect actions using lambda to pass the required actions
        qconnect(pinyin_action.triggered,
                 lambda: on_pinyin_changed(pinyin_action, zhuyin_action))
        qconnect(zhuyin_action.triggered,
                 lambda: on_zhuyin_changed(pinyin_action, zhuyin_action))

        # ------------------------------------------------------------------
        #                           Help
        # ------------------------------------------------------------------
        help_menu = QMenu("Help", mw)
        submenu.addMenu(help_menu)

        # Create actions for the Help nested submenu
        github_action = QAction("Running through a bug ?", mw)
        about_action = QAction("About", mw)

        # Add actions to Help submenu
        help_menu.addAction(github_action)
        help_menu.addAction(about_action)


        qconnect(about_action.triggered, get_display_about_dialog)
        qconnect(github_action.triggered, open_github)


        # ==================================================================
        # Editor dialog methods
        # ==================================================================

        setup_editor_ruby_button()

    except ImportError:
        # When we are running tests or we are outside Anki env
        pass


init_addon()
