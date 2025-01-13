# ==================================================================
# addon/utils/versions.py
# ==================================================================
# Handles Anki version compatibility checking using version bounds
# defined in about.toml configuration.
# ==================================================================

from aqt import mw
from aqt.utils import showWarning
from anki.utils import point_version
from .about import AddonInfo


def get_point_version(version_str: str) -> int:
    """
    Convert version string to point version number.
    Handles modern Anki version format (23.10, 24.12, etc.)
    Returns a comparable integer (e.g., "24.11" -> 2411)
    """
    parts = version_str.split('.')
    if len(parts) != 2:
        raise ValueError(f"Unsupported version format: {version_str}")

    year = int(parts[0])
    month = int(parts[1])
    return (year * 100) + month


def check_anki_version() -> bool:
    """
    Check if current Anki version is compatible with add-on.
    Uses version bounds from about.toml configuration.
    """
    addon_info = AddonInfo()
    current = point_version()

    try:
        min_point = get_point_version(addon_info.min_version)
        max_point = get_point_version(addon_info.max_version)

        # Convert current version (from point_version) to YY.MM format
        year = current // 10000
        month = (current % 10000) // 100
        current_comparable = (year * 100) + month
        current_display = f"{year}.{month}"

        if not (min_point <= current_comparable <= max_point):
            showWarning(
                f"[{addon_info.name}]:\n"
                f"This add-on requires Anki {addon_info.min_version} to {addon_info.max_version}.\n"
                f"Your version: {current_display}\n\n"
                "Please update either Anki or the add-on to a compatible version."
            )
            return False
        return True

    except (AttributeError, ValueError, IndexError) as e:
        showWarning(
            f"[{addon_info.name}]:\n"
            f"Error reading version information from add-on configuration: {str(e)}"
        )
        return False