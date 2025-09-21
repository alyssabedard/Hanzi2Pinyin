
<div align="center">
<h1 style="font-family: monospace;">Hanzi2Pinyin - Development Guide</h1>
</div>

More info: [Anki add-on writing guide](https://addon-docs.ankiweb.net/).

## Requirements
- [Poetry](https://python-poetry.org/docs/#installation)
- [Anki](https://apps.ankiweb.net/) - recent versions


## Project Structure
The `requirements.txt` is used for bundling dependencies in `addon/lib/` directory with Makefile commands. For development, use Poetry.

## Poetry Commands

| Command                  | Description                                      |
|--------------------------|--------------------------------------------------|
| `poetry install`         | Install all dependencies from pyproject.toml     |
| `poetry shell`           | Spawn a shell within the virtual environment     |
| `poetry lock`            | Generate poetry.lock file with exact versions    |
| `poetry update`          | Update all dependencies to their latest versions |
| `poetry show --outdated` | Display packages with updates available          |
| `poetry init`            | Create a new pyproject.toml file                 |
| `exit`                   | Exit the Poetry virtual environment              |

> **Note**: This project uses `package-mode = false` in Poetry configuration (_pyproject.toml_) to manage dependencies only.

## Makefile Commands

| Command                | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make help`            | Show help and available commands                                                                                                                                                                                                                                                                                                                                                                                           |
| `make check-os`        | Show detected OS and paths                                                                                                                                                                                                                                                                                                                                                                                                 |
| `make sync`            | Sync addon to Anki directory                                                                                                                                                                                                                                                                                                                                                                                               |
| `make anki`            | Start Anki with debug console                                                                                                                                                                                                                                                                                                                                                                                              |
| `make sync-and-run`    | Syncs addon files to your Anki addons directory and starts Anki. This allows you to store the repository anywhere on your system - the command will copy contents to the appropriate Anki add-on directory based on your OS. Before running, verify paths in the Makefile match your system (Windows: %APPDATA%/Anki2/addons21, macOS: ~/Library/Application Support/Anki2/addons21, Linux: ~/.local/share/Anki2/addons21) |
| `make clean-deps`      | Clean dependencies in addon/lib/                                                                                                                                                                                                                                                                                                                                                                                           |
| `make install-deps`    | Install dependencies from requirements.txt to addon/lib/                                                                                                                                                                                                                                                                                                                                                                   |
| `make update-deps`     | Update dependencies                                                                                                                                                                                                                                                                                                                                                                                                        |
| `make ankiaddon`       | Create .ankiaddon package                                                                                                                                                                                                                                                                                                                                                                                                  |
| `make check-ankiaddon` | Check contents of .ankiaddon                                                                                                                                                                                                                                                                                                                                                                                               |
| `make tag`             | Create new tag (prompts for version)                                                                                                                                                                                                                                                                                                                                                                                       |
| `make retag`           | Delete and recreate tag (prompts for version)                                                                                                                                                                                                                                                                                                                                                                              |

## Running Anki with Debug Console

For development, run Anki from the terminal to see debug output:

| OS | Command |
|---------|-------------|
| macOS | `/Library/Application Support/AnkiProgramFiles/.venv/bin/anki`|
| Linux | `anki` |
| Windows | `"C:\Program Files\Anki\anki.exe"` |

macOS- before Anki launcher: `/Applications/Anki.app/Contents/MacOS/anki` 


## Packaging

### Creating Release Package

| Command | Description |
|---------|-------------|
| `make ankiaddon` | Create .ankiaddon package |
| `make check-ankiaddon` | Verify package contents |

## Notes
- Always run Anki from terminal during development for debug output
- The `requirements.txt` is used specifically for bundling dependencies, not for development (check `install-deps` Make command)
- Use Poetry for managing development environment
- Restart Anki after making changes to the addon

## Troubleshooting





