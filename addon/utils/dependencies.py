# ==================================================================
# addon/utils/dependencies.py
# ==================================================================
# This module manages Python package dependencies that are bundled with
# the addon. It adds the lib directory to Python's import path so
# bundled packages can be imported by other modules.
# ==================================================================

from pathlib import Path
import sys
import logging
logging.basicConfig(level=logging.INFO)

# Path resolution for dependencies
# Path(__file__)              -> /path/to/addon/utils/dependencies.py
# Path(__file__).parent      -> /path/to/addon/utils/
# Path(__file__).parent.parent -> /path/to/addon/
ADDON_ROOT = Path(__file__).parent.parent

# Add lib directory to path for vendor packages
# VENDOR_DIR resolves to /path/to/addon/lib/
# This directory contains third-party packages like pypinyin and jieba
VENDOR_DIR = ADDON_ROOT / "lib"

# Insert vendor directory at start of Python's import path
# This ensures Python finds our bundled packages first
# before looking in system-wide locations
sys.path.insert(0, str(VENDOR_DIR))

# Tree visualization of dependency resolution:
# addon/                     <- ADDON_ROOT (parent.parent)
# ├── utils/                 <- first parent
# │   └── dependencies.py    <- __file__
# └── lib/                   <- VENDOR_DIR
#     ├── pypinyin/
#     ├── jieba/
#     └── other packages...

try:
    from pypinyin import pinyin, Style
    import jieba
    # import pycantonese


    logging.info("[Hanzi2Pinyin] - Successfully imported pypinyin, jieba")
    #print("[Hanzi2Pinyin]: Successfully imported pypinyin, jieba")
    # print("[Hanzi2Pinyin]: Successfully imported pypinyin, jieba, pycantonese")
except ImportError as e:
    #print(f"[Hanzi2Pinyin]: Error importing pypinyin: {e}")
    logging.info(f"[Hanzi2Pinyin] - Error importing pypinyin: {e}")
