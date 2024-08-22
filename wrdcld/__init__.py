from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from .font import FontWrapper
from .image import ImageWrapper
from .main import fill_next_word
from .rectangle import Rectangle
from .util import Color


# pylint: disable=unused-argument
def make_word_cloud(
    all_words: list[str],
    width: int = 500,
    height: int = 500,
    font_path: Path | None = None,
    font_color: Color = (255, 255, 0),
    font_color_func: Callable[[float], Color] | None = None,
    background_color: Color = (73, 109, 137),
    minimum_font_size: int = 10,
    maximum_font_size: int = 100,
    word_padding: int = 0,
    scaling_func: Callable[[float], float] = math.sqrt,
    mask=None,  # TODO
    seed: int | float | str | bytes | bytearray | None = None,
):
    if seed is not None:
        random.seed(seed)
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

    # Count the words
    word_counts = Counter(all_words)
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
            word, available_rectangles, image, font[required_font_size], frequency, word_padding=word_padding
        )

    return image.img
