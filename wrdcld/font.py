from collections.abc import Callable
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from .image import ImageWrapper
from .rectangle import Rectangle
from .util import Color, get_repo_root


@dataclass(frozen=True)
class FontWrapper:
    color_func: Callable[[float], Color]
    path: Path
    size: int = 1

    def color(self, frequency: float) -> Color:
        return self.color_func(frequency)

    @lru_cache(maxsize=1024)
    def get(self) -> FreeTypeFont:
        return ImageFont.truetype(str(self.path), self.size)

    @lru_cache(maxsize=1024)
    def getbbox(self, word: str) -> Rectangle:
        bbox = self.get().getbbox(word)
        return Rectangle(
            x=bbox[0], y=bbox[1], width=bbox[2] - bbox[0], height=bbox[3] - bbox[1]
        )

    def __getitem__(self, new_size: float) -> "FontWrapper":
        rounded_new_size = int(round(new_size))
        return replace(self, size=rounded_new_size)

    def get_length_of_word(self, word: str) -> float:
        return self.get().getlength(word)

    def find_fontsize_for_width(self, width: int, word: str) -> int:
        # Check if the word can fit even with the smallest font size
        test_font = replace(self, size=1)
        if test_font.get_length_of_word(word) > width:
            raise ValueError(f"Impossible to fit word '{word}' in width {width}")

        # Start with half of the initial size and step size as half of that
        fontsize = self.size / 2
        step = fontsize / 2

        # Perform binary search for the correct font size
        while step > 0.5:
            test_font = replace(self, size=int(fontsize))
            length = test_font.get_length_of_word(word=word)

            if length <= width:
                fontsize += step
            else:
                fontsize -= step

            step /= 2

        final_font = replace(self, size=int(fontsize))
        final_length = final_font.get_length_of_word(word=word)

        # Ensure the final font size fits within the width
        while final_length > width:
            fontsize -= 1
            final_font = replace(self, size=int(fontsize))
            final_length = final_font.get_length_of_word(word=word)

        return int(fontsize)

    @staticmethod
    def default_font() -> Path:
        return get_repo_root() / "fonts" / "OpenSans-Regular.ttf"


def draw_text(
    image: ImageWrapper,
    rectangle: Rectangle,
    word: str,
    font: FontWrapper,
    frequency: float,
    rotate=False,
):
    """
    Draws the text on the img with the correct orientation.
    """
    # text can sometimes have a negative bounding box, so we need to account for that
    text_bbox = font.getbbox(word)

    if rotate:
        text_image = Image.new("RGB", rectangle.rotated_ccw.wh, image.background_color)  # type: ignore
        text_draw = ImageDraw.Draw(text_image)

        text_draw.text(
            (-text_bbox.x, -text_bbox.y),
            word,
            font=font.get(),
            fill=font.color(frequency),
        )
        rotated_text_image = text_image.rotate(90, expand=True)
        image.img.paste(rotated_text_image, rectangle.xy)  # type: ignore

    else:
        image.canvas.text(
            (rectangle.x - text_bbox.x, rectangle.y - text_bbox.y),
            word,
            font=font.get(),
            fill=font.color(frequency),
        )
