from unittest import TestCase

from wrdcld.font import FontWrapper
from hypothesis import given
import hypothesis.strategies as st
from dataclasses import replace

class TestFont(TestCase):
    def test_get_default_font_path(self):
        font = FontWrapper(
            color_func=lambda _: (0, 0, 0), path=FontWrapper.default_font()
        )
        self.assertTrue(font.path.exists())

    @given(word=st.text(min_size=1, max_size=5).filter(lambda s: not s.isspace()), required_width=st.integers(min_value=10, max_value=1000))
    def test_get_font_size_for_width(self, word: str, required_width: int):
        font = FontWrapper(
            color_func=lambda _: (0, 0, 0), path=FontWrapper.default_font(), size=10000
        )

        if replace(font, size=1).get_length_of_word(word) > required_width:
            self.assertRaises(ValueError)

        new_font_size = font.find_fontsize_for_width(required_width, word)
        new_font = replace(font, size=new_font_size) 

        self.assertTrue(new_font_size > 0)
        self.assertTrue(new_font.get_length_of_word(word) <= required_width)




