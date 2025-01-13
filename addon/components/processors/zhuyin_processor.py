# ==================================================================
# addon/components/processors/zhuyin_processor.py
# ==================================================================
# Handles Zhuyin (Bopomofo) ruby text processing for Chinese characters
# Each character might have multiple zhuyin symbols (ㄓㄨㄥ)
# compared to pinyin which has single syllables (zhōng)
# TODO
# - more comments
# ==================================================================
import logging
from typing import Dict
from .base_processor import BaseRubyProcessor
from ...utils.dependencies import pinyin, Style, jieba

jieba.setLogLevel(logging.INFO)

#
class ZhuyinProcessor(BaseRubyProcessor):
    def add_ruby_notation(self, text: str) -> str:
        """
        Add zhuyin notation with correct word-context pronunciation.
        Example: 中心 -> 中[ㄓㄨㄥ]心[ㄒㄧㄣ]
        """
        words = list(jieba.cut(text))
        word_zhuyin_dict = self._create_zhuyin_mapping(words)

        result = []
        for i, char in enumerate(text):
            if self.is_chinese_char(char):
                try:
                    zhuyin_text = word_zhuyin_dict.get(i)
                    if zhuyin_text:
                        result.append(f"{char}[{zhuyin_text}]")
                        continue
                except (TypeError, ValueError) as e:
                    logging.warning(
                        f"[hanzi2zhuyin]: Error processing zhuyin for character {char} at position {i}: {e}"
                    )
                pass
            result.append(char)

        return "".join(result)

    def _create_zhuyin_mapping(self, words: list) -> Dict[int, str]:
        """
        Create a mapping of character positions to their zhuyin readings.
        Zhuyin symbols are joined together for each character.
        """
        word_zhuyin_dict = {}
        current_pos = 0

        for word in words:
            if any(self.is_chinese_char(char) for char in word):
                try:
                    # Get zhuyin for entire word
                    zhuyin_chars = pinyin(word, style=Style.BOPOMOFO)

                    # Map each character's position to its zhuyin
                    for i, char in enumerate(word):
                        if self.is_chinese_char(char):
                            # zhuyin_chars[i][0] already contains all symbols for one character
                            word_zhuyin_dict[current_pos + i] = zhuyin_chars[i][0]
                except Exception as e:
                    logging.warning(f"[hanzi2zhuyin]: Error generating zhuyin for word {word}: {e}")
            current_pos += len(word)

        return word_zhuyin_dict