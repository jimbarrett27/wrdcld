import math
from collections import Counter
from collections.abc import Callable

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
    minimum_font_size: int = 1,
    maximum_font_size: int = 100,
    word_padding: int = 0,  # TODO
    scaling_func: Callable[[float], float] = math.sqrt,  # TODO
    mask=None,  # TODO
):
    # Create a new image and font
    image = ImageWrapper(width, height, background_color)
    font = FontWrapper(color=font_color, size=maximum_font_size)

    # Handle data
    word_counts = Counter(all_words)
    _, first_count = word_counts.most_common(1)[0]
    available_rectangles = [Rectangle(width=500, height=500, x=0, y=0)]

    # Main loop
    for word, count in word_counts.most_common():
        required_font_size = maximum_font_size * math.sqrt(count / first_count)

        if required_font_size < minimum_font_size:
            break

        available_rectangles = fill_next_word(
            word, available_rectangles, image, font[required_font_size]
        )

    return image.img
