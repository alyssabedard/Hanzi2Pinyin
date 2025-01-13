
<div align="center">
<h1 style="font-family: monospace;">Hanzi2Pinyin - Development Guide</h1>
🚧 COMING SOON  🚧 
</div>

Please read [Anki add-on writing guide](https://addon-docs.ankiweb.net/).

> Note: This script has been primarily tested on macOS. 



## Table of Contents
- [Dependencies](#dependencies)
  - [Poetry](#poetry)

## Makefile Commands



## Testing
To test the script for debugging, open Anki with the following command in your terminal.

**macOS**
```
/Applications/Anki.app/Contents/MacOS/anki
```

**Windows**
```

```

**Linux**
```

```



### Poetry

**Poetry Commands**

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










