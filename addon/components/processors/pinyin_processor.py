# ==================================================================
# addon/components/processors/pinyin_processor.py
# ==================================================================
# Handles Pinyin ruby text processing for Chinese characters (hanzi)
# Supports word-context aware pinyin generation using jieba for
# word segmentation and pypinyin for pinyin conversion.
# ==================================================================
import logging
import re
from typing import Dict

from .base_processor import BaseRubyProcessor
from ...utils.dependencies import pinyin, Style, jieba

jieba.setLogLevel(logging.INFO)  # Suppress jieba's dictionary loading messages

class PinyinProcessor(BaseRubyProcessor):
    """
    Processor for adding pinyin ruby notation to Chinese text
    """

    def add_ruby_notation(self, text: str) -> str:
        """
        Add pinyin notation with correct word-context pronunciation.
        Example: 你好 -> 你[nǐ]好[hǎo]
        """
        # Use jieba to split text into proper Chinese words for context
        words = list(jieba.cut(text))

        # Create dictionary mapping character positions to their correct pinyin
        word_pinyin_dict = self._create_pinyin_mapping(words)

        # Build final text with pinyin notation
        result = []
        for i, char in enumerate(text):
            if self.is_chinese_char(char):
                try:
                    pinyin_text = word_pinyin_dict.get(i)
                    if pinyin_text:
                        result.append(f"{char}[{pinyin_text}]")
                        continue
                except (TypeError, ValueError) as e:
                    logging.warning(
                        f"[hanzi2pinyin]: Error processing pinyin for character {char} at position {i}: {e}"
                    )
                pass
            result.append(char)  # Keep non-Chinese characters as is

        return "".join(result)

    def _create_pinyin_mapping(self, words: list) -> Dict[int, str]:
        """
        Create a mapping of character positions to their pinyin readings
        considering word context.
        """
        word_pinyin_dict = {}
        current_pos = 0

        for word in words:
            # Check if word contains any Chinese characters
            if any(self.is_chinese_char(char) for char in word):
                try:
                    # Get pinyin for entire word to get correct context-based pronunciation
                    pinyin_chars = pinyin(word, style=Style.TONE)

                    # Map each character's position to its pinyin
                    for i, char in enumerate(word):
                        if self.is_chinese_char(char):
                            word_pinyin_dict[current_pos + i] = pinyin_chars[i][0]
                except Exception as e:
                    logging.warning(f"[hanzi2pinyin]: Error generating pinyin for word {word}: {e}")
            current_pos += len(word)

        return word_pinyin_dict