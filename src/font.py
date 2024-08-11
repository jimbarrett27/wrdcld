from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


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


def draw_text(canvas, img, rectangle, word, font, rotate=False):
    FONT_COLOR = (255, 255, 0)

    if rotate:
        text_image = Image.new("RGB", rectangle.rotated_ccw.wh, (73, 109, 137))
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), word, font=font, fill=FONT_COLOR)
        rotated_text_image = text_image.rotate(90, expand=True)
        img.paste(rotated_text_image, rectangle.xy)
        # canvas.rectangle(rectangle.xyrb)

    else:
        canvas.text(rectangle.xy, word, font=font, fill=FONT_COLOR)
        # canvas.rectangle(rectangle.xyrb)
