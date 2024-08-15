import math
from collections import Counter
from collections.abc import Callable
import random

from .font import FontWrapper
from .image import ImageWrapper
from .main import fill_next_word
from .rectangle import Rectangle


# pylint: disable=unused-argument
def make_word_cloud(
    all_words: list[str],
    width: int = 500,
    height: int = 500,
    font_color: tuple[int, int, int] = (255, 255, 0),  # TODO
    background_color: tuple[int, int, int] = (73, 109, 137),
    minimum_font_size: int = 5,
    maximum_font_size: int = 100,
    first_rectangle_fraction: float = 0.4,
    word_padding: int = 0,  # TODO
    scaling_func: Callable[[float], float] = math.sqrt,  # TODO
    mask=None,  # TODO
    seed: int | float | str | bytes | bytearray | None = None,
):
    if seed is not None:
        random.seed(seed)

    # Create a new image and font
    image = ImageWrapper(width, height, background_color)
    font = FontWrapper(color=font_color, size=maximum_font_size)

    # Handle data
    word_counts = Counter(all_words)
    first_word, first_count = word_counts.most_common(1)[0]

    initial_rectangle_width = int(width * first_rectangle_fraction)
    initial_rectangle_height = font.find_fontsize_for_width(initial_rectangle_width, first_word)

    available_rectangles = [
        Rectangle(
            width=initial_rectangle_width, 
            height=initial_rectangle_height, 
            x=random.randint(0, width - initial_rectangle_width),
            y=random.randint(0, height - initial_rectangle_height),
        )
        ]

    # Main loop
    for word, count in word_counts.most_common():
        required_font_size = maximum_font_size * math.sqrt(count / first_count)

        if required_font_size < minimum_font_size:
            break

        available_rectangles = fill_next_word(
            word, available_rectangles, image, font[required_font_size]
        )

    return image.img
