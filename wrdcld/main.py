from random import Random

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
    random_generator: Random,
    frequency: float,
    rotate: bool = False,
):
    word_height = font.size

    if not rotate:
        text_rectangle = Rectangle(
            x=random_generator.uniform(
                rectangle.x,
                rectangle.x + rectangle.width - word_length,
            ),
            y=random_generator.uniform(
                rectangle.y,
                rectangle.y + rectangle.height - word_height,
            ),
            width=word_length,
            height=word_height,
        )
    else:
        text_rectangle = Rectangle(
            x=random_generator.uniform(
                rectangle.x,
                rectangle.x + rectangle.width - word_height,
            ),
            y=random_generator.uniform(
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
    available_rectangles,
    image: ImageWrapper,
    font: FontWrapper,
    frequency: float,
    random_generator: Random,
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

    horizontal_option = (
        max(suitable_horizontal_rectangles, key=lambda x: x.area)
        if suitable_horizontal_rectangles
        else None
    )
    vertical_option = (
        max(suitable_vertical_rectangles, key=lambda x: x.area)
        if suitable_vertical_rectangles
        else None
    )

    options = []
    if horizontal_option is not None:
        options.append("horizontal")
    if vertical_option is not None:
        options.append("vertical")

    if not options:
        # print(f"skipping word '{word}', couldn't find a good rectangle")
        return available_rectangles

    if len(options) == 1:
        option = options[0]
    else:
        option = random_generator.choices(options, weights=(0.9, 0.1))[0]

    if option == "horizontal":
        available_rectangles.remove(horizontal_option)
        chosen_rectangle = horizontal_option
        rotate = False

    else:
        available_rectangles.remove(vertical_option)
        chosen_rectangle = vertical_option
        rotate = True

    text_rectangle = _fill(
        chosen_rectangle,
        image,
        word_length,
        word,
        font,
        random_generator,
        frequency,
        rotate,
    )

    fill_direction = random_generator.choice(["horizontal", "vertical"])

    # figure out new available rectangles
    fill_func = random_generator.choice(
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
