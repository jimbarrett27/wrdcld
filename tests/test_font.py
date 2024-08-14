from wrdcld.font import get_default_font_path

from unittest import TestCase


class TestFont(TestCase):
    def test_get_default_font_path(self):
        self.assertTrue(get_default_font_path().exists())
        