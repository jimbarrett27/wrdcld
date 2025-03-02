from pathlib import Path

from wrdcld import make_word_cloud

contents = Path("examples/dancingmen.txt").read_text(encoding="utf-8")

all_words = [word.strip(" \n,.!?:-&\"'[]") for word in contents.split(" ")]
all_words = [word for word in all_words if word]


def color_func(frequency):
    x = int((1 - frequency) * 200)
    return (x, x, x)


img = make_word_cloud(
    all_words=all_words,
    font_color_func=color_func,
    background_color=(255, 255, 255),
    minimum_font_size=5,
)

img.show()
