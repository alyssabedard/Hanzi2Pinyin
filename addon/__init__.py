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
# ==================================================================
DEBUG = True
if DEBUG:
    print("[Hanzi2Pinyin] Debug enabled")
    from warnings import filterwarnings
    filterwarnings("ignore")


from sys import path
from pathlib import Path

from .utils.about import AddonInfo

# Return absolute path to the directory
# containing the current Python script file
addon_path = Path(__file__).parent
if str(addon_path) not in path:
    path.append(str(addon_path))


# Uncomment to check if this file is being loaded
#from aqt.utils import showInfo
#showInfo("Addon is loading!") # Will display a pop-up window when Anki launches

from .components.ruby_button import setup_editor_ruby_button
from .utils import display_unimplemented_message, display_about_dialog, update_pronunciation_type, load_config, show_welcome_dialog


try:
    # Run normally if Anki's GUI is launched
    from aqt import mw
except ImportError:
    # Allows running tests without Anki, as test environment won't have access to Anki's GUI components.
    mw = None

if mw is not None:
    # Set Anki logger if Anki GUI running
    log = mw.addonManager.get_logger(__name__)
else:
    from logging import basicConfig, INFO, getLogger
    basicConfig(level=INFO)
    log = getLogger(__name__)


from utils.about import AddonInfo
ABOUT = AddonInfo()
log.info(f"Addon release: {ABOUT.release}")
log.info(f"Anki min supported version: {ABOUT.min_version}")
log.info(f"Addon tested version: {ABOUT.tested_version}")

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
    Initialize the addon's menu items and buttons in Anki's GUI interface.
    This function creates a submenu under Anki's Tools menu with options for:
    - Phonetics
    - Help
    """
    if mw is None:
        return  # Exit early if no Anki GUI not launched

    logs_path = mw.addonManager.logs_folder(__name__)
    log.info(f"Your logs will be stored in: {logs_path}")


    from aqt.qt import QMenu, QAction
    from aqt.utils import qconnect

    # Show welcome dialog
    #show_welcome_dialog(mw)

    # Load config at startup
    config = load_config()

    # Check version compatibility before initializing
    # log.info("Checking Anki version...")
    from .utils.versions import check_anki_version
    check_anki_version()

    # ==================================================================
    # Submenu in Anki's toolbar menu
    # ==================================================================

    submenu = QMenu("Hanzi2Pinyin", mw)
    mw.form.menuTools.addMenu(submenu)

    # ------------------------------------------------------------------
    # Add-on SUBMENU Tools/Hanzi2Pinyin
    #   Tools Menu
    #    └── Hanzi2Pinyin           # Hanzi2Pinyin submenu
    #        ├── Phonetics          # QAction
    #        ├── Help               # QAction
    # ------------------------------------------------------------------
    # - Each QAction is connected to a function using qconnect
    # - Qt methods used by Anki to connect signals to slots (event handlers):
    #       qconnect(some_action.triggered, do_something)
    #           some_action          is a signal
    #           do_something         is the function that will be called
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
    #                           Help and About
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


log.info(f"[Hanzi2Pinyin] - Initialize the addon's menu items and buttons in Anki's interface...")
init_addon()
