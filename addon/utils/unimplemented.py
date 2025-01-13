# ==================================================================
# addon/components/unimplemented.py
# ==================================================================
# Display a message that the feature isn't implemented yet
# ==================================================================

from aqt.utils import showText


def display_unimplemented_message() -> None:
    """
    Display message that feature is not implemented yet.
    """
    info_text = (
        "<center>"
        "<h3>Not implemented yet.</h3>"
        f"<p>More information on GitHub repository.</p>"
        "</center>"
    )

    showText(
        info_text,
        title="Implementation status",
        type="rich",
        minWidth=400,
        minHeight=300,
    )
