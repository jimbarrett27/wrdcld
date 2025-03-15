import random

from .font import FontWrapper, draw_text
from .image import ImageWrapper
from .rectangle import (
    Rectangle,
    fill_remaining_space_horizontal,
    fill_remaining_space_vertical,
    fill_space_around_word,
)


# pylint: disable=(too-many-positional-arguments)
def _fill(
    rectangle: Rectangle,
    image: ImageWrapper,
    word_length: float,
    word: str,
    font: FontWrapper,
    frequency: float,
    rotate: bool = False,
):
    word_height = font.size

    if not rotate:
        text_rectangle = Rectangle(
            x=random.uniform(
                rectangle.x,
                rectangle.x + rectangle.width - word_length,
            ),
            y=random.uniform(
                rectangle.y,
                rectangle.y + rectangle.height - word_height,
            ),
            width=word_length,
            height=word_height,
        )
    else:
        text_rectangle = Rectangle(
            x=random.uniform(
                rectangle.x,
                rectangle.x + rectangle.width - word_height,
            ),
            y=random.uniform(
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
        use_horizontal = random.random() < 0.5
        if use_horizontal:
            chosen_rectangle = max(suitable_horizontal_rectangles, key=lambda x: x.area)
        else:
            chosen_rectangle = max(suitable_vertical_rectangles, key=lambda x: x.area)
            rotate = True

    else:
        print(f"skipping word '{word}', couldn't find a good rectangle")
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

    fill_direction = random.choice(["horizontal", "vertical"])

    # figure out new available rectangles
    fill_func = random.choice(
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


