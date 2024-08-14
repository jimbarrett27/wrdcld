from PIL import Image, ImageDraw, ImageFont

from wrdcld.util import get_repo_root


class FontWrapper:
    def __init__(self, path=None, color=(255, 255, 0)):
        self.path = path or get_repo_root() / "fonts" / "OpenSans-Regular.ttf"

    def with_size(self, fontsize: float) -> 'FreeTypeFont':
        return ImageFont.truetype(self.path, fontsize)
    
    def length_of_word(self, fontsize: float, word: str) -> float:
        font = self.with_size(fontsize=fontsize)
        return font.getlength(word)

    def find_fontsize_for_width(self, width, word):
        fontsize = width / 2
        step = width / 2

        while step > 0.5:
            step /= 2
            
            length = self.length_of_word(fontsize=fontsize, word=word)

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
