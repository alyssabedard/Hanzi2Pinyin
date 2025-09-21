# ==================================================================
# addon/components/about.py
# ==================================================================
# Project Information Handler
# Retrieve data from about.toml and handle "About" dialog
# TODO:
# - Fix CSS
# ==================================================================
from aqt.utils import showText
from pathlib import Path
from  tomllib import load


class AddonInfo:
    """
    Handles all project-related information loaded from TOML file.
    Basic usage:
        project = AddonInfo()
        print(project.name)
        project.display_about_dialog()
    """

    def __init__(self):
        # Get the components directory where this script is located
        services_dir = Path(__file__).parent
        # Go up one level to addon directory and find the TOML file
        self.toml_path = services_dir.parent / "about.toml"
        self._load_config()

    def _load_config(self):
        """
        Loads and parses the TOML file, storing all config values
        as attributes of this class
        """
        # Read the TOML file
        with open(self.toml_path, "rb") as f:
            data = load(f)

        # Get the main sections using get() to provide empty dict if missing
        project = data.get("project", {})
        github = project.get("github", {})
        anki = project.get("anki", {})
        # maintainers = project.get("maintainers", {})

        # Basic project information
        self.name = project.get("name", "")
        self.release = project.get("release", "")
        self.description = project.get("description", "")
        self.authors = project.get("authors", [])
        self.license = project.get("license", "")
        self.homepage = project.get("homepage", "")

        # GitHub specific information
        # self.documentation = github.get("documentation", "")
        # self.repository = github.get("repository", "")
        self.issues = github.get("issues", "")
        self.feature_requests = github.get("feature-requests", "")
        self.discussions = github.get("discussions", "")

        # Anki specific information
        self.addon_id = anki.get("addon-id", "")
        self.min_version = anki.get("min-version", "")
        self.max_version = anki.get("max-version", "")
        self.tested_version = anki.get("tested-version", "")
        self.conflicts = anki.get("conflicts", [])

        # Maintainer information
        # self.primary_maintainer = maintainers.get("primary", "")
        # self.contributors = maintainers.get("contributors", [])

    def get_about_html(self):
        return f"""
        <style>
        .title {{
            text-align: center;
            color: #A692E3;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 24px;
            margin: 20px 0;
        }}

        .content {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 15px;
        }}
        </style>

        <div class="title">{self.name}</div>

        <div class="content">
            <p><strong>Addon version:</strong> {self.release}</p>
            <p><strong>Description:</strong> {self.description}</p>
            <p><strong>Author:</strong> {", ".join(self.authors)}</p>

            <p><strong>Links:</strong></p>
            <p>🏠 <a href="{self.homepage}">Homepage</a></p>
            <p>🐞 <a href="{self.issues}">Report Issues</a></p>
            <p>💫 <a href="{self.feature_requests}">Request Features</a></p>
            <p>💡 <a href="{self.discussions}">Discussions, need help?</a></p>

            <p><strong>Technical Details:</strong></p>
            <p>Add-on ID: {self.addon_id}</p>
            <p>Oldest supported Anki version for this addon release: {self.min_version}</p>
            <p>Tested on Anki version: {self.tested_version}</p>
            <p>License: {self.license}</p>
        </div>
        """

    def display_about_dialog(self):
        """
        Shows the about dialog with all project information.
        This is the main method you'll call from your addon.
        """
        showText(
            self.get_about_html(),
            title=f"About {self.name}",
            type="rich",
            minWidth=400,
            minHeight=500,
        )

    def __str__(self):
        """
        Creates a readable string representation of the project info.
        Useful for debugging or logging.
        """
        return f"""
        Project: {self.name}
        Version: {self.release}
        Description: {self.description}
        Authors: {', '.join(self.authors)}

        Anki Details:
        - Addon ID: {self.addon_id}
        - Min Version: {self.min_version}
        - Tested Version: {self.tested_version}
        """


# ===================================
# Helper Functions
# ===================================
def get_project_info() -> AddonInfo:
    """
    Helper function to create a AddonInfo object.
    Usage:
        project = get_project_info()
        project.display_about_dialog()
    """
    return AddonInfo()


def display_about_dialog():
    """
    Helper function to directly show the about dialog.
    Usage:
        display_about_dialog()
    """
    project_info = AddonInfo()
    project_info.display_about_dialog()