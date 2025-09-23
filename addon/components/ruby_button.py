# ==================================================================
# addon/components/ruby_button.py
# ==================================================================
# Handles Ruby text button functionality in the editor
# ==================================================================
from aqt.utils import showInfo, tooltip
from aqt.gui_hooks import editor_did_init_buttons
from aqt.editor import Editor
from aqt import mw
from pathlib import Path


from .ruby_processor import RubyProcessor

class RubyHandler:
    """
    Handles ruby operations in different contexts
    """

    def __init__(self):
        self.processor = RubyProcessor()

    def handle_editor_button_click(self, editor: Editor) -> None:
        """
        Handle single field conversion in editor (both Add and Browse)
        """
        if not editor.note:
            showInfo("[Hanzi2Pinyin]: No note selected!")
            return

        if editor.currentField is None:
            showInfo("[Hanzi2Pinyin]: Please select a field first!")
            return

        try:
            # Get field content
            field_name = editor.note.keys()[editor.currentField]
            field_content = editor.note[field_name]

            # Use core processor
            new_content = self.processor.toggle_ruby_text(field_content)

            # Update depending on context
            editor.note[field_name] = new_content

            # Different handling for Add vs Browse
            if editor.parentWindow.__class__.__name__ == "AddCards":
                # Handle Add dialog specifics
                editor.loadNoteKeepingFocus()
            else:
                # Handle Browse dialog specifics
                mw.col.update_note(editor.note)
                editor.loadNoteKeepingFocus()

            tooltip("Ruby notation toggled", period=500)

        except Exception as e:
            showInfo(f"Error: {str(e)}")


def add_ruby_button(buttons: list, editor: Editor, handler: RubyHandler) -> None:
    """
    Add Ruby conversion button to Anki's editor interface.

    Args:
        buttons (list): Current list of editor buttons
        editor (Editor): Anki editor instance
        handler (RubyHandler): Handler for ruby text operations

    Returns:
       list: Updated list of buttons with ruby button added
    """

    btn = editor.addButton(
        icon=None,
        cmd="Hanzi2Pinyin",
        func=lambda e: handler.handle_editor_button_click(e),
        tip="Hanzi2Pinyin 你[nǐ]好[hǎo]",
        label="中[zhōng]",
        keys=None,
        disables=False,
    )
    buttons.append(btn)
    #return buttons


def setup_editor_ruby_button() -> None:
    """
    Attach function to the hook that gets triggered
    when the editor's buttons are being initialized.

    It's like telling Anki: "When you're setting up editor buttons,
    please also run the add_ruby_button function."
    """
    handler = RubyHandler()
    editor_did_init_buttons.append(
        lambda buttons, editor: add_ruby_button(buttons, editor, handler)
    )
