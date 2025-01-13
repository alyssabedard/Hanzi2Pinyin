# ==================================================================
# tests/test_pinyin_processor.py
# ==================================================================
# Test suite for PinyinProcessor class, focusing on core functionality
# without Anki dependencies. Tests pinyin ruby notation processing for
# Chinese characters.
#
# Tests cover:
#   - Basic ruby notation detection
#   - Unicode ranges handling
#   - Context-dependent pronunciations
#   - Mixed text processing (Chinese + non-Chinese)
#   - Ruby notation toggle (add/remove)
#   - Complex sentence processing
#
# Example sentences provided by Claude AI to test various Chinese
# character pronunciations and contexts.
# ==================================================================
import pytest
from addon.components.processors.pinyin_processor import PinyinProcessor


@pytest.fixture
def processor():
    return PinyinProcessor()


def test_basic_ruby_pinyin(processor):
    assert not processor.has_ruby_notation("你好")
    assert processor.has_ruby_notation("你[nǐ]好[hǎo]")


def test_unicode_ranges_pinyin(processor):
    test_cases = [
        # Basic CJK (0x4e00-0x9fff)
        ("你好", "你[nǐ]好[hǎo]"),              # Common characters
        # Extension A (0x3400-0x4dbf)
        ("㐀㐁", "㐀[qiū]㐁[tiàn]"),            # Less common characters
        # Extension B (0x20000-0x2a6df)
        ("𠀀", "𠀀[hē]"),                      # Rare characters
    ]

    for input_text, expected in test_cases:
        result = processor.add_ruby_notation(input_text)
        assert result == expected, f"Failed for input: {input_text}"


def test_context_dependent_pronunciations_pinyin(processor):
    """
    Test characters that have different pronunciations based on context
    """
    test_cases = [
        ("了解", "了[liǎo]解[jiě]"),        # liǎo (understand)
        ("完了", "完[wán]了[le]"),          # le (completed)
        ("长城", "长[cháng]城[chéng]"),     # cháng (long)
        ("成长", "成[chéng]长[zhǎng]"),     # zhǎng (grow)
        ("音乐", "音[yīn]乐[yuè]"),         # yuè (music)
        ("快乐", "快[kuài]乐[lè]"),         # lè (happy)
    ]

    for input_text, expected in test_cases:
        result = processor.add_ruby_notation(input_text)
        assert result == expected, f"Failed for input: {input_text}"


def test_mixed_text_pinyin(processor):
    """
    Test handling of mixed Chinese and non-Chinese text
    """
    test_cases = [
        ("Hello 你好", "Hello 你[nǐ]好[hǎo]"),
        ("你好123好的", "你[nǐ]好[hǎo]123好[hǎo]的[de]"),
        ("ABC你好DEF", "ABC你[nǐ]好[hǎo]DEF"),
    ]

    for input_text, expected in test_cases:
        result = processor.add_ruby_notation(input_text)
        assert result == expected, f"Failed for input: {input_text}"


def test_toggle_ruby_pinyin(processor):
    """
    Test adding and removing ruby notation
    """
    original = "你好世界"
    with_ruby = processor.add_ruby_notation(original)
    assert processor.has_ruby_notation(with_ruby)

    removed = processor.remove_ruby_notation(with_ruby)
    assert removed == original
    assert not processor.has_ruby_notation(removed)


def test_complex_sentence_pinyin(processor):
    """
    Test a complex sentence with multiple pronunciation variations
    """
    input_text = "我长大以后学音乐，看不了太难的乐谱。"
    expected = "我[wǒ]长[zhǎng]大[dà]以[yǐ]后[hòu]学[xué]音[yīn]乐[yuè]，看[kàn]不[bù]了[liǎo]太[tài]难[nán]的[de]乐[yuè]谱[pǔ]。"

    result = processor.add_ruby_notation(input_text)
    assert result == expected, "Failed complex sentence test"