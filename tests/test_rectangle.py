from unittest import TestCase
from hypothesis import given, settings, Verbosity
import hypothesis.strategies as st
from string import ascii_letters, digits, punctuation

from wrdcld.rectangle import Rectangle, _remove_small_rectangles, MIN_RECTANGLE_SIDE_LENGTH, fill_remaining_space_vertical, fill_remaining_space_horizontal, fill_space_around_word
from wrdcld.font import get_default_font_path
from PIL import Image, ImageDraw, ImageFont
import math


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

@st.composite
def text_image_and_rectangle_strategy(draw):
    """
    Generates an image with text and a rectangle that contains the text
    """
    # don't generate purely whitespace
    text = draw(st.text(alphabet=ascii_letters+digits+punctuation, min_size=1, max_size=10))

    font_path = get_default_font_path()
    font_size = draw(st.integers(min_value=50, max_value=100))
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = font.getbbox(text)

    img_rectangle = Rectangle(width=math.ceil(font.getlength(text)), height=font_size, x=0, y=0)
    img = Image.new("RGB", (img_rectangle.width, img_rectangle.height), (255, 255, 255))
    canvas = ImageDraw.Draw(img)

    canvas.text((-text_bbox[0], -text_bbox[1]), text, font=font, fill=(0, 0, 0))

    return img, img_rectangle

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

    @given(text_image_and_rectangle=text_image_and_rectangle_strategy(), fill_direction=st.sampled_from(["vertical", "horizontal"]))
    def test_fill_around_word(self, text_image_and_rectangle, fill_direction):
        """
        Test that after filling the space around a word, that there are no pixels of the font color in the new rectangles
        """
        img, img_rectangle = text_image_and_rectangle
        new_rectangles = fill_space_around_word(img, img_rectangle, fill_direction=fill_direction, background_color=(255, 255, 255)) 
        for r in new_rectangles:
            self.assertTrue(r.is_inside(img_rectangle))

            img_on_rectangle = img.crop(r.xyrb)
            image_section_data = img_on_rectangle.getdata()

            if not all([d != (0, 0, 0) for d in image_section_data]):
                print("! " * 20)    
                breakpoint()
            self.assertTrue(all([d != (0, 0, 0) for d in image_section_data]))


        