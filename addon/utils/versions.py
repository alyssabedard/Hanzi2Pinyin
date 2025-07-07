# ==================================================================
# addon/utils/versions.py
# ==================================================================
# Handles Anki version compatibility checking using version bounds
# defined in about.toml configuration.
#
# ==================================================================

from aqt import mw
from aqt.utils import showWarning
from anki.utils import point_version
from .about import AddonInfo
import re
import logging
log = getattr(mw.addonManager, "getLogger", logging.getLogger)(__name__)


def get_point_version(version_str: str) -> int:
    """
    Convert version string to point version number.
    Handles:
    - Anki format (23.10 → 2310)
    - Poetry constraints (^25.2 → 2502)
    - Tested version (25.2.5 → 2502)
    """
    # Strip constraint symbols (^~>=<) and patch versions
    clean_version = re.sub(r'[\^~>=<]', '', version_str).split('.')

    if len(clean_version) >= 2:
        year = int(clean_version[0])
        month = int(clean_version[1])
        return (year * 100) + month
    raise ValueError(f"Unsupported version format: {version_str}")


def calculate_max_version(constraint: str) -> str:
    """
    Convert Poetry constraint to Anki-compatible max version.
    Examples:
    "^25.2" → "25.12" (full year support)
    "~25.2" → "25.8" (6 months support)
    "25.2" → "25.2" (exact version)
    """
    log.info("Constraint: %r", getattr(constraint, "__dict__", repr(constraint)))
    if constraint.startswith('^'):
        year = constraint.split('.')[0].lstrip('^')
        return f"{year}.12"
    elif constraint.startswith('~'):
        year, month = constraint.lstrip('~').split('.')[:2]
        return f"{year}.{min(int(month) + 6, 12)}"
    else:
        return constraint.split('.')[0] + '.' + constraint.split('.')[1]


def check_anki_version() -> bool:
    addon_info = AddonInfo()
    log.info("Addon info: %r", getattr(addon_info, "__dict__", repr(addon_info)))
    current = point_version()
    log.info("Current point version (YYMMPatch): %r", getattr(current, "__dict__", repr(current)))

    try:

        # Get base minimum version (always required)
        min_point = get_point_version(addon_info.min_version)

        # Calculate effective max version
        max_version = (calculate_max_version(addon_info.max_version)
                       if any(c in addon_info.max_version for c in '^~')
                       else addon_info.max_version)
        max_point = get_point_version(max_version)

        # Convert current Anki version
        year = current // 10000
        month = (current % 10000) // 100
        current_comparable = (year * 100) + month
        current_display = f"{year}.{month:02d}"

        # Version check logic
        if current_comparable < min_point:
            showWarning(
                f"[{addon_info.name}]:\n"
                f"This add-on requires Anki {addon_info.min_version} or newer.\n"
                f"Your version: {current_display}\n\n"
                "Please update Anki to a compatible version."
            )
            return False

        if current_comparable > max_point:
            showWarning(
                f"[{addon_info.name}]:\n"
                f"This add-on is tested up to Anki {addon_info.tested_version}.\n"
                f"Your version: {current_display}\n\n"
                "Some features may not work correctly - check for updates."
            )
            return True

        return True

    except Exception as e:
        showWarning(
            f"[{addon_info.name}]:\n"
            f"Version check error: {str(e)}\n"
            f"Config: min={getattr(addon_info, 'min_version', '?')} "
            f"max={getattr(addon_info, 'max_version', '?')}"
        )
        return True