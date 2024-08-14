from unittest import TestCase
from hypothesis import given
import hypothesis.strategies as st

from wrdcld.rectangle import Rectangle, _remove_small_rectangles, MIN_RECTANGLE_SIDE_LENGTH, fill_remaining_space_vertical, fill_remaining_space_horizontal

@st.composite
def rectangle_strategy(draw):
    """
    generate a simple rectangle
    """
    width = draw(st.integers(min_value=1, max_value=100))
    height = draw(st.integers(min_value=1, max_value=100))
    x = draw(st.integers(min_value=0, max_value=100))
    y = draw(st.integers(min_value=0, max_value=100))
    return Rectangle(width=width, height=height, x=x, y=y)

@st.composite
def nested_rectangle_strategy(draw):
    """
    generate two rectangles, one inside the other
    """
    outer_rectangle = draw(rectangle_strategy())

    width = draw(st.integers(min_value=1, max_value=outer_rectangle.width))
    height = draw(st.integers(min_value=1, max_value=outer_rectangle.height))

    inner_rectangle = Rectangle(
        width=width,
        height=height,
        x = draw(st.integers(min_value=outer_rectangle.x, max_value=outer_rectangle.right-width)),
        y = draw(st.integers(min_value=outer_rectangle.y, max_value=outer_rectangle.bottom-height))
    )

    return outer_rectangle, inner_rectangle


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

    @given(rectangles=st.lists(rectangle_strategy(), min_size=1))
    def test_remove_small_rectangles(self, rectangles):
        rectangles = _remove_small_rectangles(rectangles)
        for r in rectangles:
            self.assertTrue(r.width >= MIN_RECTANGLE_SIDE_LENGTH)
            self.assertTrue(r.height >= MIN_RECTANGLE_SIDE_LENGTH)


    @given(nested_rectangles=nested_rectangle_strategy())
    def test_fill_remaining_space_vertical(self, nested_rectangles):
        outer, inner = nested_rectangles
        self.assertTrue(inner.is_inside(outer))
        new_rectangles = fill_remaining_space_vertical(outer, inner)
        for r in new_rectangles:
            self.assertTrue(r.is_inside(outer))
            self.assertFalse(r.is_inside(inner))
            self.assertFalse(r.overlaps(inner))

    @given(nested_rectangles=nested_rectangle_strategy())
    def test_fill_remaining_space_horizontal(self, nested_rectangles):
        outer, inner = nested_rectangles
        self.assertTrue(inner.is_inside(outer))
        new_rectangles = fill_remaining_space_horizontal(outer, inner)
        for r in new_rectangles:
            self.assertTrue(r.is_inside(outer))
            self.assertFalse(r.is_inside(inner))
            self.assertFalse(r.overlaps(inner))


        