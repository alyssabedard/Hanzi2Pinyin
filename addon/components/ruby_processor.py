# ==================================================================
# addon/components/ruby_processor.py
# ==================================================================
# Handles Ruby text processing for Chinese characters (hanzi)
# Ruby notation: 你[nǐ]好[hǎo], that will be read by Anki through the
# Furigana field {{furigana:YourField}}.
# Documentation:
# https://docs.ankiweb.net/templates/fields.html?highlight=furigana#ruby-characters
# TODO:
# - add comments
# ==================================================================
from .processors.factory import RubyProcessorFactory


class RubyProcessor:

    @classmethod
    def toggle_ruby_text(cls, text: str) -> str:
        processor = RubyProcessorFactory.get_processor()
        return processor.toggle_ruby_text(text)

    @classmethod
    def add_ruby_notation(cls, text: str) -> str:
        processor = RubyProcessorFactory.get_processor()
        return processor.add_ruby_notation(text)

    @classmethod
    def remove_ruby_notation(cls, text: str) -> str:
        processor = RubyProcessorFactory.get_processor()
        return processor.remove_ruby_notation(text)


