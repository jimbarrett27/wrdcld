from unittest import TestCase

from wrdcld.font import FontWrapper


class TestFont(TestCase):
    def test_get_default_font_path(self):
        font = FontWrapper(
            color_func=lambda _: (0, 0, 0), path=FontWrapper.default_font()
        )
        self.assertTrue(font.path.exists())
