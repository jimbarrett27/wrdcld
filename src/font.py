from pathlib import Path
from PIL import ImageFont


FONT_PATH = Path(r"C:\\Windows\\Fonts\\Verdanab.ttf")
# FONT_PATH = Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf")


def find_fontsize_for_width(width, word):
    fontsize = width / 2
    step = width / 2

    while step > 0.5:
        step /= 2
        font = ImageFont.truetype(FONT_PATH, fontsize)
        length = font.getlength(word)

        if length < width:
            fontsize += step
        else:
            fontsize -= step

    return fontsize


def draw_text(canvas, rectangle, word, font):
    canvas.text((rectangle.x, rectangle.y), word, fill=(255, 255, 0), font=font)
