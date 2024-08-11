import random
from PIL import ImageFont

from .font import FONT_PATH, draw_text
from .rectangle import (
    Rectangle,
    fill_remaining_space_horizontal,
    fill_remaining_space_vertical,
)


def fill_next_word(word, required_font_size, available_rectangles, canvas):
    font = ImageFont.truetype(FONT_PATH, required_font_size)
    word_length = font.getlength(word)

    suitable_horizontal_rectangles = [
        rectangle
        for rectangle in available_rectangles
        if rectangle.width >= word_length and rectangle.height >= required_font_size
    ]

    # suitable_vertical_rectangles = []
    # for rectangle in available_rectangles:
    #    if rectangle.height < word_length:
    #        continue
    #    if rectangle.width < required_font_size:
    #        continue
    #    suitable_vertical_rectangles.append(rectangle)

    horizontal_option = (
        max(suitable_horizontal_rectangles, key=lambda x: x.area)
        if suitable_horizontal_rectangles
        else None
    )
    # vertical_option = max(suitable_vertical_rectangles, key=lambda x: x.area) if suitable_vertical_rectangles else None

    if horizontal_option is None:  # and vertical_option is None:
        # print(f"skipping word '{word}', couldn't find a good rectangle")
        return available_rectangles

    chosen_rectangle = horizontal_option

    text_rectangle = Rectangle(
        x=random.uniform(
            chosen_rectangle.x,
            chosen_rectangle.x + chosen_rectangle.width - word_length,
        ),
        y=random.uniform(
            chosen_rectangle.y,
            chosen_rectangle.y + chosen_rectangle.height - required_font_size,
        ),
        width=word_length,
        height=required_font_size,
    )

    draw_text(canvas, text_rectangle, word, font)

    # figure out new available rectangles
    fill_func = random.choice(
        [fill_remaining_space_horizontal, fill_remaining_space_vertical]
    )
    new_available_rectangles = fill_func(chosen_rectangle, text_rectangle)

    # remove the chosen rectangle and add the new ones
    available_rectangles.remove(chosen_rectangle)
    return available_rectangles + new_available_rectangles
