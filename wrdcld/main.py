import random

from .font import FontWrapper, draw_text
from .image import ImageWrapper
from .rectangle import (
    Rectangle,
    fill_remaining_space_horizontal,
    fill_remaining_space_vertical,
    fill_space_around_word,
)


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
    available_rectangles: list[Rectangle],
    image: ImageWrapper,
    font: FontWrapper,
    frequency,
    word_padding: int,
):
    word_length = font.get_length_of_word(word)

    suitable_horizontal_rectangles = []
    suitable_vertical_rectangles = []
    for rectangle in available_rectangles:
        padded_rectangle = rectangle.get_subrectangle_with_padding(word_padding)

        if (
            padded_rectangle.width >= word_length
            and padded_rectangle.height >= font.size
        ):
            suitable_horizontal_rectangles.append(rectangle)
        if (
            padded_rectangle.height >= word_length
            and padded_rectangle.width >= font.size
        ):
            suitable_vertical_rectangles.append(rectangle)

    direction_options = []
    if len(suitable_horizontal_rectangles) == 0:
        direction_options.append("horizontal")
    if len(suitable_vertical_rectangles) == 0:
        direction_options.append("vertical")

    if not direction_options:
        # print(f"skipping word '{word}', couldn't find a good rectangle")
        return available_rectangles

    if len(direction_options) == 1:
        chosen_direction = direction_options[0]
    else:
        chosen_direction = random.choices(direction_options, weights=(0.9, 0.1))[0]

    if chosen_direction == "horizontal":
        horizontal_choice = max(suitable_horizontal_rectangles, key=lambda x: x.area)

        available_rectangles.remove(horizontal_choice)
        chosen_rectangle = horizontal_choice.get_subrectangle_with_padding(word_padding)
        text_rectangle = _fill(
            chosen_rectangle, image, word_length, word, font, frequency
        )

    else:
        vertical_choice = max(suitable_vertical_rectangles, key=lambda x: x.area)
        available_rectangles.remove(vertical_choice)
        chosen_rectangle = vertical_choice.get_subrectangle_with_padding(word_padding)
        text_rectangle = _fill(
            chosen_rectangle,
            image,
            word_length,
            word,
            font,
            frequency,
            rotate=True,
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
