from pathlib import Path

from wrdcld import make_word_cloud

contents = Path("examples/dancingmen.txt").read_text(encoding="utf-8")

all_words = [word.strip(" \n,.!?:-&\"'[]") for word in contents.split(" ")]
all_words = [word for word in all_words if word]

make_word_cloud(
    all_words=all_words,
    font_color=(0, 0, 0),
    background_color=(255, 255, 255),
    minimum_font_size=5,
).show()
