# ==================================================================
# addon/utils/config.py
# ==================================================================
# This module manages configuration persistence for the Hanzi2Pinyin addon.
# It provides functions to load, save and update user preferences like
# pronunciation type (pinyin/zhuyin) using Anki's addon configuration
# system.
# ==================================================================

from aqt import mw
from pathlib import Path

# Get root addon package path
# Path(__file__)              -> /path/to/addon/utils/config.py
# Path(__file__).parent      -> /path/to/addon/utils/
# Path(__file__).parent.parent -> /path/to/addon/
ADDON_ROOT = Path(__file__).parent.parent
# Gets the addon folder name by extracting the last part of the path
# If ADDON_ROOT is /path/to/addon/, ADDON_NAME will be 'addon'
ADDON_NAME = ADDON_ROOT.name

# Tree visualization of path resolution:
# addon/                        <- ADDON_ROOT (parent.parent)
# ├── utils/                    <- first parent
# │   └── config.py             <- __file__

# Add lib directory and its subdirectories to path


def load_config():
    """
    Load the addon configuration or create default if none exists.
    """
    config = mw.addonManager.getConfig(ADDON_NAME)
    if config is None:
        config = {
            'pronunciation_type': 'pinyin',
            'first_launch': True,
        }
        mw.addonManager.writeConfig(ADDON_NAME, config)
        # try:
        #     with open(get_config_path(), 'r', encoding='utf-8') as f:
        #         stored_config = json.load(f)
        #         config.update(stored_config)
        # except FileNotFoundError:
        #     save_config(config)
    return config


def save_config(config):
    """
    Save the current configuration.
    """
    mw.addonManager.writeConfig(ADDON_NAME, config)

def mark_first_launch_complete():
    """
    Mark that the addon has been launched before
    """
    config = load_config()
    config['first_launch'] = False
    save_config(config)


def update_pronunciation_type(pronunciation_type):
    """
    Update the pronunciation type in config.
    """
    config = load_config()
    config['pronunciation_type'] = pronunciation_type
    save_config(config)

def get_pronunciation_type():
    """
    Get the current pronunciation type from config.
    """
    config = load_config()
    return config.get('pronunciation_type', 'pinyin') # Default = pinyin