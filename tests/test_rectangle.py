from src.rectangle import Rectangle
from unittest import TestCase


class TestRectangle(TestCase):
    def test_basic_properties(self):
        r = Rectangle(width=5, height=7, x=1, y=2)
        self.assertEqual(r.xy, (1, 2))
        self.assertEqual(r.wh, (5, 7))
        self.assertEqual(r.right, 6)
        self.assertEqual(r.bottom, 9)
        self.assertEqual(r.xyrb, (1, 2, 6, 9))
        self.assertEqual(r.area, 35)

    def test_rotation(self):
        r = Rectangle(width=10, height=3, x=20, y=30)
        r_ccw = r.rotated_ccw

        self.assertEqual(r_ccw.x, 20)
        self.assertEqual(r_ccw.y, 23)
        self.assertEqual(r_ccw.width, 3)
        self.assertEqual(r_ccw.height, 10)

        self.assertEqual(r.area, r_ccw.area)
