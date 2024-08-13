from collections import Counter
import math
from PIL import Image, ImageDraw

from .main import fill_next_word
from .rectangle import Rectangle


def make_word_cloud(
    all_words,
    width=500,
    height=500,
    background_color=(73, 109, 137),
    maximum_font_size=100,
):
    # Create a new image
    img = Image.new("RGB", (width, height), color=background_color)
    canvas = ImageDraw.Draw(img)

    word_counts = Counter(all_words)

    _, first_count = word_counts.most_common(1)[0]

    available_rectangles = [Rectangle(width=500, height=500, x=0, y=0)]
    for word, count in word_counts.most_common(500):
        required_font_size = maximum_font_size * math.sqrt(count / first_count)

        if required_font_size < 1:
            break

        available_rectangles = fill_next_word(
            word, required_font_size, available_rectangles, img, canvas
        )


    for rectangle in available_rectangles:
        canvas.rectangle(rectangle.xyrb)

    return img
