from PIL import Image, ImageDraw, ImageFont

from wrdcld.util import get_repo_root


def get_default_font_path():
    return get_repo_root() / "fonts" / "OpenSans-Regular.ttf"


def find_fontsize_for_width(width, word):
    fontsize = width / 2
    step = width / 2

    font_path = get_default_font_path()
    while step > 0.5:
        step /= 2

        font = ImageFont.truetype(font_path, fontsize)
        length = font.getlength(word)

        if length < width:
            fontsize += step
        else:
            fontsize -= step

    return fontsize


def draw_text(canvas, img, rectangle, word, font, rotate=False):
    """
    Draws the text on the img with the correct orientation.
    """
    FONT_COLOR = (255, 255, 0)

    # text can sometimes have a negative bounding box, so we need to account for that
    text_bbox = font.getbbox(word)

    if rotate:
        text_image = Image.new("RGB", rectangle.rotated_ccw.wh, (73, 109, 137))
        text_draw = ImageDraw.Draw(text_image)

        text_draw.text((-text_bbox[0], -text_bbox[1]), word, font=font, fill=FONT_COLOR)
        rotated_text_image = text_image.rotate(90, expand=True)
        img.paste(rotated_text_image, rectangle.xy)
        # canvas.rectangle(rectangle.xyrb)

    else:
        canvas.text(
            (rectangle.x - text_bbox[0], rectangle.y - text_bbox[1]),
            word,
            font=font,
            fill=FONT_COLOR,
        )
        # canvas.rectangle(rectangle.xyrb)
