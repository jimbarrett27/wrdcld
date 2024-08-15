from PIL import Image, ImageDraw


class ImageWrapper:
    def __init__(self, width: int, height: int, background_color: tuple[int, int, int]):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.img = Image.new("RGB", (width, height), color=background_color)
        self.canvas = ImageDraw.Draw(self.img)
