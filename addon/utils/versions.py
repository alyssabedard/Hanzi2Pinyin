# ==================================================================
# addon/utils/versions.py
# ==================================================================
# Handles Anki version compatibility checking using version bounds
# defined in about.toml configuration.
#
# ==================================================================

from aqt import mw
from aqt.utils import showInfo
from anki.utils import point_version

from .. import log
from .. import ABOUT
# ADDON_NAME must be the add-on FOLDER name (e.g. "77106192" when installed
# from AnkiWeb), not ABOUT.name: getConfig() reads addons21/<folder>/config.json
# and returns None when that folder doesn't exist.
from .config import ADDON_NAME


#TESTED_ANKI_VERSION = "25.07"
TESTED_ANKI_VERSION = ABOUT.tested_version
# The config key keeps the display name so it is stable across install folders
KEY = f"{ABOUT.name}_addon_warning_{TESTED_ANKI_VERSION.replace('.', '')}"

def _get_config() -> dict:
    # Load the config dictionary for the addon, never None
    return mw.addonManager.getConfig(ADDON_NAME) or {}

def is_first_run_for_version():
    # Return false if first run
    return not _get_config().get(KEY, False)

def set_warned_flag():
    config = _get_config()
    config[KEY] = True
    # Write the updated config back to Anki’s profile storage
    # so it persists between sessions
    mw.addonManager.writeConfig(ADDON_NAME, config)

def to_readable(v):
    year = v // 10000
    month = (v // 100) % 100
    #patch = v % 100
    return f"{year}.{month:02d}"

def check_anki_version() -> bool:
    # The version check is informational only and must never prevent
    # the add-on from loading
    try:
        anki_curr_version = to_readable(point_version())

        if anki_curr_version != TESTED_ANKI_VERSION and is_first_run_for_version():
            showInfo(
                f"Hanzi2Pinyin was tested on Anki {TESTED_ANKI_VERSION}, but you are running {anki_curr_version}.\n"
                "If you run into any issues, please raise an issue on GitHub."
            )
            set_warned_flag()
        log.info(f"Config: {_get_config()}")
    except Exception as e:
        log.error(f"Anki version check failed: {e}")
    return True

