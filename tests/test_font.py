from unittest import TestCase

from wrdcld.font import FontWrapper


class TestFont(TestCase):
    def test_get_default_font_path(self):
        font = FontWrapper()
        self.assertTrue(font.path.exists())
