# ==================================================================
# addon/components/processors/base_processor.py
# ==================================================================
# Base processor class for ruby text operations.
# Provides common functionality for handling Chinese character detection
# and ruby notation manipulation (adding/removing/toggling).
#
# Ruby notation format: 你[nǐ]好[hǎo]
# Used by Anki through {{furigana:Field}} syntax
# ==================================================================
import re
from abc import ABC, abstractmethod
from typing import Pattern


class BaseRubyProcessor(ABC):
    """
    Abstract base class for ruby text processors.
    Handles common operations for both pinyin and zhuyin processors.
    """

    # Unicode ranges for Chinese characters that pypinyin can handle
    # https://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode

    # Basic CJK range (most common characters)
    BASIC_CJK_START = 0x4E00    # Common Chinese characters start
    BASIC_CJK_END = 0x9FFF      # Common Chinese characters end

    # Extension A range (rare characters)
    EXT_A_START = 0x3400
    EXT_A_END = 0x4DBF

    # Extension B range (very rare characters)
    EXT_B_START = 0x20000
    EXT_B_END = 0x2A6DF

    # Regex pattern for Chinese character detection using the ranges above
    # Combines Basic CJK and Extension A ranges for matching
    CHINESE_CHAR_PATTERN: str = (
        f"[{chr(BASIC_CJK_START)}-{chr(BASIC_CJK_END)}"
        f"{chr(EXT_A_START)}-{chr(EXT_A_END)}]"
    )

    # Note: Extension B not included in the default pattern due to being less common

    @classmethod
    def is_chinese_char(cls, char: str) -> bool:
        """
        Check if a character is within the supported Chinese Unicode ranges.

        Args:
            char: Single character to check

        Returns:
            bool: True if character is within supported Chinese ranges
        """
        code_point = ord(char)
        return (
                (cls.BASIC_CJK_START <= code_point <= cls.BASIC_CJK_END)
                or (cls.EXT_A_START <= code_point <= cls.EXT_A_END)
                or (cls.EXT_B_START <= code_point <= cls.EXT_B_END)
        )

    @abstractmethod
    def add_ruby_notation(self, text: str) -> str:
        """
        Add ruby notation to Chinese text.
        Must be implemented by concrete processor classes.

        Args:
            text: Text containing Chinese characters

        Returns:
            str: Text with ruby notation added
        """
        pass

    def toggle_ruby_text(self, text: str) -> str:
        """
        Toggle ruby notation - add if not present, remove if present.

        Args:
            text: Text to toggle ruby notation on

        Returns:
            str: Text with ruby notation toggled
        """
        if self.has_ruby_notation(text):
            return self.remove_ruby_notation(text)
        return self.add_ruby_notation(text)

    def has_ruby_notation(self, text: str) -> bool:
        """
        Check if text contains ruby notation.
        Looks for pattern: Chinese character + [pronunciation]

        Args:
            text: Text to check for ruby notation

        Returns:
            bool: True if ruby notation is found
        """
        pattern = f"({self.CHINESE_CHAR_PATTERN})\[[^]]+]"
        return bool(re.search(pattern, text))

    def remove_ruby_notation(self, text: str) -> str:
        """
        Remove ruby notation while preserving Chinese characters.

        Args:
            text: Text containing ruby notation

        Returns:
            str: Text with ruby notation removed

        Example:
            你[nǐ]好[hǎo] -> 你好
        """
        # Remove notation after Chinese characters
        pattern = f"({self.CHINESE_CHAR_PATTERN})\[[^]]*]"
        text = re.sub(pattern, r"\1", text)
        # Remove any remaining bracketed content
        text = re.sub(r"\[[^]]*]", "", text)
        return text