# ==================================================================
# # addon/components/processors/factory.py
# ==================================================================
#  TODO
# - Fix comments
# - JyutpingProcessor
# ==================================================================

from ...utils.config import get_pronunciation_type
from .zhuyin_processor import ZhuyinProcessor
from .pinyin_processor import PinyinProcessor
# from .jyutping_processor import JyutpingProcessor

class RubyProcessorFactory:
    """
    Factory class that creates ruby processor objects based on user configuration.

    Centralizes object creation and allows switching between
    different processor implementations (Pinyin/Zhuyin) without modifying client code.

    Returns:
        - PinyinProcessor: When config is set to 'pinyin'
        - ZhuyinProcessor: When config is set to 'zhuyin'

    Example:
        processor = RubyProcessorFactory.get_processor()
        result = processor.add_ruby_notation("你好")  # Will use pinyin or zhuyin based on config
    """
    @staticmethod
    def get_processor():
        """
        Create and return appropriate processor based on user configuration.
        Default to PinyinProcessor if config is not set.
        """
        pronunciation_type = get_pronunciation_type()
        if pronunciation_type == 'zhuyin':
            return ZhuyinProcessor()
        # elif pronunciation_type == 'jyutping':
        #     return JyutpingProcessor()
        return PinyinProcessor()  # default