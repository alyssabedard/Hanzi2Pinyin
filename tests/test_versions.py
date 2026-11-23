# ==================================================================
# tests/test_versions.py
# ==================================================================
# Test suite for addon/utils/versions.py (Anki version check).
#
# Anki's getConfig()/writeConfig() identify an add-on by its install
# FOLDER name, not its display name, and getConfig() returns None for a
# folder that doesn't exist. The folder depends on how it was installed:
#   - AnkiWeb:                addons21/77106192/  (add-on ID)
#   - Local dev (make sync):  addons21/Hanzi2Pinyin/
# The version check only reads the config when the running Anki differs
# from the tested version, and it must never prevent the add-on from
# loading.
#
# These tests don't need Anki installed: Anki's modules (aqt, anki) are
# replaced with small fake versions, and versions.py is loaded by itself
# instead of importing the whole add-on.
# ==================================================================
import importlib.util
import sys
import types
from pathlib import Path

import pytest

VERSIONS_PY = Path(__file__).parent.parent / "addon" / "utils" / "versions.py"
PKG = "_h2p_versions_test"

ANKIWEB_FOLDER = "77106192"   # Folder name AnkiWeb installs to
TESTED_VERSION = "26.09"


class FakeAddonManager:
    """Mimics aqt.addons.AddonManager: configs are keyed by FOLDER name,
    and getConfig() returns None for a folder that doesn't exist."""

    def __init__(self, configs):
        self.configs = configs
        self.writes = []

    def getConfig(self, name):
        conf = self.configs.get(name)
        return dict(conf) if conf is not None else None

    def writeConfig(self, name, conf):
        self.writes.append(name)
        self.configs[name] = dict(conf)


@pytest.fixture
def load_versions(monkeypatch):
    """Return a function that loads versions.py with the given Anki state."""

    def _load(configs, anki_point_version, folder=ANKIWEB_FOLDER):
        manager = FakeAddonManager(configs)
        shown = []

        aqt = types.ModuleType("aqt")
        aqt.mw = types.SimpleNamespace(addonManager=manager)
        aqt_utils = types.ModuleType("aqt.utils")
        aqt_utils.showInfo = shown.append
        anki = types.ModuleType("anki")
        anki_utils = types.ModuleType("anki.utils")
        anki_utils.point_version = lambda: anki_point_version

        # Parent package standing in for addon/ (provides log and ABOUT)
        pkg = types.ModuleType(PKG)
        pkg.__path__ = []
        pkg.log = types.SimpleNamespace(info=lambda *a, **k: None,
                                        error=lambda *a, **k: None)
        pkg.ABOUT = types.SimpleNamespace(name="Hanzi2Pinyin",
                                          tested_version=TESTED_VERSION)
        utils_pkg = types.ModuleType(f"{PKG}.utils")
        utils_pkg.__path__ = []
        # addon/utils/config.py derives ADDON_NAME from the install folder
        config_mod = types.ModuleType(f"{PKG}.utils.config")
        config_mod.ADDON_NAME = folder

        for name, mod in {
            "aqt": aqt, "aqt.utils": aqt_utils,
            "anki": anki, "anki.utils": anki_utils,
            PKG: pkg, f"{PKG}.utils": utils_pkg,
            f"{PKG}.utils.config": config_mod,
        }.items():
            monkeypatch.setitem(sys.modules, name, mod)

        spec = importlib.util.spec_from_file_location(f"{PKG}.utils.versions", VERSIONS_PY)
        versions = importlib.util.module_from_spec(spec)
        monkeypatch.setitem(sys.modules, spec.name, versions)
        spec.loader.exec_module(versions)
        return versions, manager, shown

    return _load


def test_ankiweb_install_untested_version_does_not_crash(load_versions):
    # Installed from AnkiWeb, running an Anki newer than the tested version
    versions, manager, shown = load_versions(
        {ANKIWEB_FOLDER: {"pronunciation_type": "pinyin"}}, anki_point_version=261004)

    assert versions.check_anki_version() is True
    assert len(shown) == 1
    assert "26.10" in shown[0]
    # The warned flag is saved to the add-on's real folder
    assert manager.writes == [ANKIWEB_FOLDER]
    assert manager.configs[ANKIWEB_FOLDER][versions.KEY] is True
    assert manager.configs[ANKIWEB_FOLDER]["pronunciation_type"] == "pinyin"


def test_warning_only_shown_once(load_versions):
    configs = {ANKIWEB_FOLDER: {"pronunciation_type": "pinyin"}}
    versions, _, shown = load_versions(configs, anki_point_version=261004)
    versions.check_anki_version()
    versions.check_anki_version()
    assert len(shown) == 1


def test_tested_version_shows_no_warning(load_versions):
    versions, manager, shown = load_versions(
        {ANKIWEB_FOLDER: {"pronunciation_type": "pinyin"}}, anki_point_version=260904)
    assert versions.check_anki_version() is True
    assert shown == []
    assert manager.writes == []


def test_local_dev_install_folder(load_versions):
    # `make sync` installs to addons21/Hanzi2Pinyin/
    versions, manager, shown = load_versions(
        {"Hanzi2Pinyin": {"pronunciation_type": "pinyin"}},
        anki_point_version=261004, folder="Hanzi2Pinyin")
    assert versions.check_anki_version() is True
    assert len(shown) == 1
    assert manager.writes == ["Hanzi2Pinyin"]


def test_missing_config_never_blocks_loading(load_versions):
    # Even if Anki returns no config at all, the add-on must still load
    versions, _, _ = load_versions({}, anki_point_version=261004)
    assert versions.check_anki_version() is True
