from logging import getLogger
import math
from collections import Counter
from collections.abc import Callable

from .font import FontWrapper, draw_text
from .image import ImageWrapper
from .rectangle import (
    Rectangle,
    fill_remaining_space_horizontal,
    fill_remaining_space_vertical,
    fill_space_around_word,
)
from .util import get_random_state

LOGGER = getLogger(__name__)


# pylint: disable=unused-argument
from __future__ import annotations

import math
from collections import Counter
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from PIL.Image import Image

from .font import FontWrapper
from .image import ImageWrapper
from .main import fill_next_word
from .rectangle import Rectangle
from .util import Color, get_random_state


# pylint: disable=(unused-argument, too-many-positional-arguments)
def make_word_cloud(
    all_words: list[str] | Counter,
    width: int = 500,
    height: int = 500,
    font_path: Path | None = None,
    font_color: Color = (255, 255, 0),
    font_color_func: Callable[[float], Color] | None = None,
    background_color: Color = (73, 109, 137),
    minimum_font_size: int = 10,
    maximum_font_size: int = 100,
    word_padding: int = 0,  # TODO
    scaling_func: Callable[[float], float] = math.sqrt,
    mask: Image | None = None,  # TODO
    seed: int | None = None,
) -> Image:

    _ = get_random_state(reseed=True, seed=seed)

    # Asserts
    assert len(all_words) > 0, "No words in list"
    assert width > 0, "Width must be a positive number (in pixels)"
    assert height > 0, "Height must be a positive number (in pixels)"
    assert (
        0 < minimum_font_size < maximum_font_size
    ), "Invalid font sizes, must be positive (in pixels)"
    assert (
        font_color is not None or font_color_func is not None
    ), "Must specify a fixed font color or function"
    assert isinstance(all_words, (list, Counter)), "Word supply must be list or Counter"

    # Count the words
    if isinstance(all_words, list):
        word_counts = Counter(all_words)
    else:
        word_counts = all_words
    first_word, first_count = word_counts.most_common(1)[0]

    # Create a new image and font
    font_path = font_path or FontWrapper.default_font()
    font_color_func = font_color_func or (lambda _: font_color)
    image = ImageWrapper(width, height, background_color)
    font = FontWrapper(
        path=font_path, color_func=font_color_func, size=maximum_font_size
    )

    actual_max_fontsize = font.find_fontsize_for_width(width, first_word)

    if actual_max_fontsize < maximum_font_size:
        maximum_font_size = actual_max_fontsize
        font = replace(font, size=actual_max_fontsize)

    available_rectangles = [Rectangle(width=width, height=height, x=0, y=0)]
    for word, count in word_counts.most_common():
        frequency = count / first_count
        required_font_size = maximum_font_size * scaling_func(frequency)

        if required_font_size < minimum_font_size:
            break

        available_rectangles = fill_next_word(
            word, available_rectangles, image, font[required_font_size], frequency
        )

    return image.img

def _fill(
    rectangle: Rectangle,
    image: ImageWrapper,
    word_length: float,
    word: str,
    font: FontWrapper,
    frequency: float,
    rotate: bool = False,
):

    random_state = get_random_state()

    word_height = font.size

    if not rotate:
        text_rectangle = Rectangle(
            x=random_state.uniform(
                rectangle.x,
                rectangle.x + rectangle.width - word_length,
            ),
            y=random_state.uniform(
                rectangle.y,
                rectangle.y + rectangle.height - word_height,
            ),
            width=word_length,
            height=word_height,
        )
    else:
        text_rectangle = Rectangle(
            x=random_state.uniform(
                rectangle.x,
                rectangle.x + rectangle.width - word_height,
            ),
            y=random_state.uniform(
                rectangle.y,
                rectangle.y + rectangle.height - word_length,
            ),
            width=word_height,
            height=word_length,
        )

    draw_text(image, text_rectangle, word, font, frequency, rotate=rotate)

    return text_rectangle


def fill_next_word(
    word: str,
    available_rectangles: list,
    image: ImageWrapper,
    font: FontWrapper,
    frequency: float,
):

    random_state = get_random_state()

    available_rectangles = available_rectangles.copy()

    word_length = font.get_length_of_word(word)

    suitable_horizontal_rectangles = [
        rectangle
        for rectangle in available_rectangles
        if rectangle.width >= word_length and rectangle.height >= font.size
    ]

    suitable_vertical_rectangles = [
        rectangle
        for rectangle in available_rectangles
        if rectangle.height >= word_length and rectangle.width >= font.size
    ]

    rotate = False
    if suitable_horizontal_rectangles and not suitable_vertical_rectangles:
        chosen_rectangle = max(suitable_horizontal_rectangles, key=lambda x: x.area)

    elif suitable_vertical_rectangles and not suitable_horizontal_rectangles:
        chosen_rectangle = max(suitable_vertical_rectangles, key=lambda x: x.area)
        rotate = True

    elif suitable_horizontal_rectangles and suitable_vertical_rectangles:
        use_horizontal = random_state.random() < 0.5
        if use_horizontal:
            chosen_rectangle = max(suitable_horizontal_rectangles, key=lambda x: x.area)
        else:
            chosen_rectangle = max(suitable_vertical_rectangles, key=lambda x: x.area)
            rotate = True

    else:
        LOGGER.warning("skipping word '%s', couldn't find a good rectangle", word)
        return available_rectangles

    available_rectangles.remove(chosen_rectangle)

    text_rectangle = _fill(
        chosen_rectangle,
        image,
        word_length,
        word,
        font,
        frequency,
        rotate=rotate,
    )

    fill_direction = random_state.choice(["horizontal", "vertical"])

    # figure out new available rectangles
    fill_func = random_state.choice(
        [fill_remaining_space_horizontal, fill_remaining_space_vertical]
    )
    new_available_rectangles = fill_func(chosen_rectangle, text_rectangle)

    available_rectangles_around_word = fill_space_around_word(
        image, text_rectangle, fill_direction
    )

    return (
        available_rectangles
        + new_available_rectangles
        + available_rectangles_around_word
    )
