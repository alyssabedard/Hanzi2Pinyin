# Detect operating system
# https://docs.ankiweb.net/files.html
# https://docs.ankiweb.net/files.html#program-files
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    # Windows paths
    ANKI_ADDON_DIR := $(APPDATA)/Anki2/addons21
    ANKI_PATH := "C:/Program Files/Anki/anki.exe"
    RM_CMD := rd /s /q
    CP_CMD := xcopy /E /I /Y
    MKDIR_CMD := mkdir
    RMDIR_CMD := rmdir /s /q
    # Windows color codes
    BLUE := [34m
    YELLOW := [33m
    GREEN := [32m
    NC := [0m
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        DETECTED_OS := Linux
        # Linux paths
        ANKI_ADDON_DIR := $(HOME)/.local/share/Anki2/addons21
        ANKI_PATH := anki
        RM_CMD := rm -rf
        CP_CMD := cp -r
        MKDIR_CMD := mkdir -p
        RMDIR_CMD := rm -rf
    endif
    ifeq ($(UNAME_S),Darwin)
        DETECTED_OS := MacOS
        # MacOS paths
        ANKI_ADDON_DIR := $(HOME)/Library/Application Support/Anki2/addons21
        # Anki Path Before Launcher
        #ANKI_PATH := /Applications/Anki.app/Contents/MacOS/anki
        ANKI_PATH := $(HOME)/Library/Application Support/AnkiProgramFiles/.venv/bin/anki
        RM_CMD := rm -rf
        CP_CMD := cp -r
        MKDIR_CMD := mkdir -p
        RMDIR_CMD := rm -rf
    endif
    # Unix-like color codes
    BLUE := \033[34m
    YELLOW := \033[33m
    GREEN := \033[32m
    NC := \033[0m
endif

# Common variables
ADDON_NAME := Hanzi2Pinyin
PYTHON_CMD := python
ifeq ($(DETECTED_OS),Windows)
    PYTHON_CMD := python.exe
endif


.DEFAULT_GOAL := help

.PHONY: help sync anki sync-and-run clean-deps install-deps update-deps  check-os tag retag ankiaddon check-zip check-ankiaddon check-contents

help:
	@echo ""
	@echo "$(BLUE)=== Hanzi2Pinyin Anki Add-on Development Commands ===$(NC)"
	@echo "----------------------------------------------------"
	@echo "$(YELLOW)System Information:$(NC)"
	@echo "  make check-os     - Show detected OS and paths"
	@echo ""
	@echo "$(YELLOW)Development Commands:$(NC)"
	@echo "  make help         - Show this help message"
	@echo "  make sync         - Sync 'addon/' to Anki directory"
	@echo "  make anki         - Start Anki with debug console"
	@echo "  make sync-and-run - Sync addon and start Anki"
	@echo ""
	@echo "$(YELLOW)Dependency Management:$(NC)"
	@echo "  make clean-deps    - Remove all dependencies"
	@echo "  make install-deps  - Install dependencies"
	@echo "  make update-deps   - Update to latest versions"
	@echo ""
	@echo "$(YELLOW)GitHub Releases:$(NC)"
	@echo "  make tag   		- Create a new tag (GitHub workflows)"
	@echo "  make retag  		- Delete and recreate a tag (GitHub workflows)"
	@echo "  make ankiaddon"
	@echo "  make check-zip"
	@echo ""





# Check OS configuration
check-os:
	@echo "$(BLUE)Detected OS: $(DETECTED_OS)$(NC)"
	@echo "$(BLUE)Anki Add-on Directory: $(ANKI_ADDON_DIR)$(NC)"
	@echo "$(BLUE)Anki Path: $(ANKI_PATH)$(NC)"

# Dependency management
install-deps:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PYTHON_CMD) -m pip install -r requirements.txt --target ./addon/lib --upgrade
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

clean-deps:
	@echo "$(YELLOW)Cleaning dependency directory...$(NC)"
	$(RM_CMD) ./addon/lib/*
	@echo "$(GREEN)Dependencies cleaned successfully!$(NC)"


update-deps: clean-deps install-deps
	@echo "$(GREEN)Dependencies updated successfully!$(NC)"


# Sync addon to Anki directory
sync:
sync:
	@echo "$(BLUE)Syncing addon to Anki...$(NC)"
ifeq ($(DETECTED_OS),Windows)
	$(RM_CMD) "$(ANKI_ADDON_DIR)/$(ADDON_NAME)" > nul 2>&1 || true
	$(MKDIR_CMD) "$(ANKI_ADDON_DIR)" > nul 2>&1 || true
else
	$(RM_CMD) "$(ANKI_ADDON_DIR)/$(ADDON_NAME)" 2>/dev/null || true
	$(MKDIR_CMD) "$(ANKI_ADDON_DIR)" 2>/dev/null || true
endif
	$(CP_CMD) addon "$(ANKI_ADDON_DIR)/$(ADDON_NAME)"
ifeq ($(DETECTED_OS),Windows)
	@for /r "$(ANKI_ADDON_DIR)/$(ADDON_NAME)" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
else
	@find "$(ANKI_ADDON_DIR)/$(ADDON_NAME)" -type d -name "__pycache__" -exec rm -rf {} +
endif
	@echo "$(GREEN)✨ Sync complete! ✨$(NC)"

# Launch Anki
anki:
	@echo "$(BLUE)Starting Anki...$(NC)"
	@echo "Launching from: $(ANKI_PATH)"
	@"$(ANKI_PATH)"

# Combined sync and launch
sync-and-run: sync anki


# Command to delete and recreate a tag
# It will prompt: Enter version (e.g., 2025.11.02):
# Will delete existing tag and create new one
retag:
	@read -p "Enter version (e.g., 2025.10.31): " version; \
	if [ -n "$$version" ]; then \
		echo "Deleting tag v$$version..."; \
		git push --delete origin "v$$version" 2>/dev/null || echo "Remote tag doesn't exist"; \
		git tag -d "v$$version" 2>/dev/null || echo "Local tag doesn't exist"; \
		echo "Creating new tag v$$version..."; \
		git tag "v$$version" && \
		git push origin "v$$version" && \
		echo "Successfully created and pushed tag v$$version" || \
		echo "Failed to create/push tag"; \
	else \
		echo "No version provided"; \
	fi

# Command to create a new tag
# It will prompt: Enter version (e.g., 1.0.0):
# If tag already exists, it will tell you to use retag
tag:
	@read -p "Enter version (e.g., 2025.12.31): " version; \
	if [ -n "$$version" ]; then \
		if git rev-parse "v$$version" >/dev/null 2>&1; then \
			echo "Error: Tag v$$version already exists. Use 'make retag' to recreate it."; \
			exit 1; \
		else \
			echo "Creating new tag v$$version..."; \
			git tag "v$$version" && \
			git push origin "v$$version" && \
			echo "Successfully created and pushed tag v$$version" || \
			echo "Failed to create/push tag"; \
		fi \
	else \
		echo "No version provided"; \
	fi

ankiaddon:
	@echo "$(BLUE)Creating .ankiaddon package...$(NC)"
	@find addon -type d -name "__pycache__" -exec rm -rf {} +
	cd addon && zip -r ../Hanzi2Pinyin.ankiaddon * -x "**/__pycache__/*"
	@echo "$(GREEN)✨ Created Hanzi2Pinyin.ankiaddon ✨$(NC)"

# Command to verify contents
check-contents:
	@echo "$(BLUE)Checking .ankiaddon contents...$(NC)"
	unzip -l Hanzi2Pinyin.ankiaddon

check-zip:
	@echo "$(BLUE)Creating check zip file...$(NC)"
	cd addon && zip -r ../addon_check.zip * --exclude "*__pycache__*" "*.pyc"
	@echo "$(GREEN)✨ Created addon_check.zip for verification ✨$(NC)"

check-ankiaddon:
	@echo "$(BLUE)Checking .ankiaddon contents...$(NC)"
	unzip -l Hanzi2Pinyin.ankiaddon