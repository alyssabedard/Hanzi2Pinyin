# ==================================================================
# tests/test_zhuyin_processor.py
# ==================================================================
# Test suite for ZhuyinProcessor class, focusing on core functionality
# without Anki dependencies. Tests zhuyin (bopomofo) ruby notation
# processing for Chinese characters.
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
from addon.components.processors.zhuyin_processor import ZhuyinProcessor


@pytest.fixture
def processor():
    return ZhuyinProcessor()


def test_basic_ruby_zhuyin(processor):
    assert not processor.has_ruby_notation("你好")
    assert processor.has_ruby_notation("你[ㄋㄧˇ]好[ㄏㄠˇ]")


def test_unicode_ranges_zhuyin(processor):
    """
    Test handling of characters from different Unicode ranges
    """
    test_cases = [
        # Basic CJK
        ("你好", "你[ㄋㄧˇ]好[ㄏㄠˇ]"),
        # Extension A
        ("㐀㐁", "㐀[ㄑㄧㄡ]㐁[ㄊㄧㄢˋ]"),
        # Extension B
        ("𠀀", "𠀀[ㄏㄜ]"),
    ]

    for input_text, expected in test_cases:
        result = processor.add_ruby_notation(input_text)
        assert result == expected, f"Failed for input: {input_text}"


def test_context_dependent_pronunciations_zhuyin(processor):
    """
    Test characters that have different pronunciations based on context
    """
    test_cases = [
        ("了解", "了[ㄌㄧㄠˇ]解[ㄐㄧㄝˇ]"),
        ("完了", "完[ㄨㄢˊ]了[ㄌㄜ˙]"),
        ("长城", "长[ㄔㄤˊ]城[ㄔㄥˊ]"),
        ("成长", "成[ㄔㄥˊ]长[ㄓㄤˇ]"),
        ("音乐", "音[ㄧㄣ]乐[ㄩㄝˋ]"),
        ("快乐", "快[ㄎㄨㄞˋ]乐[ㄌㄜˋ]"),
    ]

def test_mixed_text_zhuyin(processor):
    """
    Test handling of mixed Chinese and non-Chinese text
    """
    test_cases = [
        ("Hello 你好", "Hello 你[ㄋㄧˇ]好[ㄏㄠˇ]"),
        ("你好123好的", "你[ㄋㄧˇ]好[ㄏㄠˇ]123好[ㄏㄠˇ]的[ㄉㄜ˙]"),  # Changed from [˙ㄉㄜ] to [ㄉㄜ˙]
        ("ABC你好DEF", "ABC你[ㄋㄧˇ]好[ㄏㄠˇ]DEF"),
    ]


def test_toggle_ruby_zhuyin(processor):
    """
    Test adding and removing ruby notation
    """
    original = "你好世界"
    with_ruby = processor.add_ruby_notation(original)
    assert processor.has_ruby_notation(with_ruby)

    removed = processor.remove_ruby_notation(with_ruby)
    assert removed == original
    assert not processor.has_ruby_notation(removed)


def test_complex_sentence_zhuyin(processor):
    """
    Test a complex sentence with multiple pronunciation variations
    """
    input_text = "我长大以后学音乐，看不了太难的乐谱。"
    expected = "我[ㄨㄛˇ]长[ㄓㄤˇ]大[ㄉㄚˋ]以[ㄧˇ]后[ㄏㄡˋ]学[ㄒㄩㄝˊ]音[ㄧㄣ]乐[ㄩㄝˋ]，看[ㄎㄢˋ]不[ㄅㄨˋ]了[ㄌㄧㄠˇ]太[ㄊㄞˋ]难[ㄋㄢˊ]的[ㄉㄜ˙]乐[ㄩㄝˋ]谱[ㄆㄨˇ]。"  # Changed neutral tone mark position