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


#TESTED_ANKI_VERSION = "25.07"
TESTED_ANKI_VERSION = ABOUT.tested_version
ADDON_NAME = ABOUT.name
KEY = f"{ADDON_NAME}_addon_warning_{TESTED_ANKI_VERSION.replace('.', '')}"

def is_first_run_for_version():
    # Load the config dictionary for the addon
    config = mw.addonManager.getConfig(ADDON_NAME)
    # Return false if first run
    return not config.get(KEY, False)

def set_warned_flag():
    # Load the config dictionary for the addon
    config = mw.addonManager.getConfig(ADDON_NAME)
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
    anki_curr_version = to_readable(point_version())

    if anki_curr_version != TESTED_ANKI_VERSION and is_first_run_for_version():
        showInfo(
            f"Hanzi2Pinyin was tested on Anki {TESTED_ANKI_VERSION}, but you are running {anki_curr_version}.\n"
            "If you run into any issues, please raise an issue on GitHub."
        )
        set_warned_flag()
    config = mw.addonManager.getConfig(ADDON_NAME)
    log.info(f"Config: {config}")
    return True

