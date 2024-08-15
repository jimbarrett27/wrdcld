import math
from unittest import TestCase

import hypothesis.strategies as st
from hypothesis import given

from wrdcld.font import FontWrapper
from wrdcld.image import ImageWrapper
from wrdcld.rectangle import (
    MIN_RECTANGLE_SIDE_LENGTH,
    Rectangle,
    _remove_small_rectangles,
    fill_remaining_space_horizontal,
    fill_remaining_space_vertical,
    fill_space_around_word,
)


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
        x=draw(
            st.integers(
                min_value=outer_rectangle.x, max_value=outer_rectangle.right - width
            )
        ),
        y=draw(
            st.integers(
                min_value=outer_rectangle.y, max_value=outer_rectangle.bottom - height
            )
        ),
    )

    return outer_rectangle, inner_rectangle


@st.composite
def text_image_and_rectangle_strategy(draw):
    """
    Generates an image with text and a rectangle that contains the text
    """

    text = draw(st.text(min_size=1, max_size=10))

    font_size = draw(st.integers(min_value=5, max_value=100))
    font = FontWrapper(size=font_size)
    text_bbox = font.getbbox(text)

    img_rectangle = Rectangle(
        width=math.ceil(font.get_length_of_word(text)), height=font_size, x=0, y=0
    )

    image = ImageWrapper(
        width=img_rectangle.width,
        height=img_rectangle.height,
        background_color=(255, 255, 255),
    )

    image.canvas.text(
        (-text_bbox.x, -text_bbox.y), text, font=font.get(), fill=(0, 0, 0)
    )

    return image, img_rectangle


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

    @given(
        text_image_and_rectangle=text_image_and_rectangle_strategy(),
        fill_direction=st.sampled_from(["vertical", "horizontal"]),
    )
    def test_fill_around_word(self, text_image_and_rectangle, fill_direction):
        """
        Test that after filling the space around a word, that there are no pixels of the font color in the new rectangles
        """
        image, img_rectangle = text_image_and_rectangle
        new_rectangles = fill_space_around_word(
            image,
            img_rectangle,
            fill_direction=fill_direction,
        )
        for r in new_rectangles:
            self.assertTrue(r.is_inside(img_rectangle))

            img_on_rectangle = image.img.crop(r.xyrb)
            image_section_data = img_on_rectangle.getdata()
            self.assertTrue(all(d != (0, 0, 0) for d in image_section_data))
