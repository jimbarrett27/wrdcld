import os
import re
from pathlib import Path

from wrdcld import make_word_cloud

FOLDER_PATH = Path("wrdcld")

all_text = ""
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".py"):
        with open(FOLDER_PATH / filename, "r", encoding="utf-8") as f:
            all_text += f.read()

cleaned_text = re.sub(r"[^a-zA-Z0-9_\s]", " ", all_text)
all_words = cleaned_text.split()


img = make_word_cloud(
    all_words=all_words,
    minimum_font_size=5,
    word_padding=3,
)

img.show()
