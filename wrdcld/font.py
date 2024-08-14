from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from wrdcld.util import get_repo_root
from wrdcld.rectangle import Rectangle


@dataclass(frozen=True)
class FontWrapper:
    path: Path = get_repo_root() / "fonts" / "OpenSans-Regular.ttf"
    size: int = (1,)
    color: tuple[int, int, int] = (255, 255, 0)

    @lru_cache(maxsize=1024)
    def get(self):
        return ImageFont.truetype(self.path, self.size)

    @lru_cache(maxsize=1024)
    def getbbox(self, word: str):
        bbox = self.get().getbbox(word)
        return Rectangle(
            x=bbox[0], y=bbox[1], width=bbox[2] - bbox[0], height=bbox[3] - bbox[1]
        )

    def __getitem__(self, new_size: int):
        return replace(self, size=new_size)  

    def get_length_of_word(self, word: str) -> float:
        return self.get().getlength(word)

    def find_fontsize_for_width(self, width, word):
        fontsize = width / 2
        step = width / 2

        while step > 0.5:
            step /= 2

            length = self[fontsize].get_length_of_word(word=word)

            if length < width:
                fontsize += step
            else:
                fontsize -= step

        return fontsize


def draw_text(canvas, img, background_color, rectangle, word, font, rotate=False):
    """
    Draws the text on the img with the correct orientation.
    """
    # text can sometimes have a negative bounding box, so we need to account for that
    text_bbox = font.getbbox(word)

    if rotate:
        text_image = Image.new("RGB", rectangle.rotated_ccw.wh, background_color)
        text_draw = ImageDraw.Draw(text_image)

        text_draw.text(
            (-text_bbox.x, -text_bbox.y), word, font=font.get(), fill=font.color
        )
        rotated_text_image = text_image.rotate(90, expand=True)
        img.paste(rotated_text_image, rectangle.xy)

    else:
        canvas.text(
            (rectangle.x - text_bbox.x, rectangle.y - text_bbox.y),
            word,
            font=font.get(),
            fill=font.color,
        )
