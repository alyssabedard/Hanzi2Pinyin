
## [2026.11.22]

### Resolves [#10](https://github.com/alyssabedard/Hanzi2Pinyin/issues/10) and [#11](https://github.com/alyssabedard/Hanzi2Pinyin/issues/11)

#### Bug Fixes:
- Fix add-on failing to load on Anki versions other than 25.09 when installed from AnkiWeb (`'NoneType' object has no attribute 'get'`). The version check now looks up the config by the add-on's install folder name and can no longer prevent the add-on from loading

#### Development and tooling:
- Update tested Anki version to 26.09 and dev dependencies `anki`/`aqt` to 26.9.4
- Add unit tests for the Anki version check
- Makefile: fall back to `/Applications/Anki.app` on macOS when the Anki launcher isn't installed, and use `python3` for `install-deps` on macOS/Linux
- Fix macOS Anki path in development docs and outdated supported versions in AnkiWeb upload notes
- Clean up README and AnkiWeb description: remove dropped planned features (Jyutping/Cantonese, Xiao'erjing, Sandhi) and outdated sections



