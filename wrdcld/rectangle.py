import math
from dataclasses import dataclass

from .image import ImageWrapper

MIN_RECTANGLE_SIDE_LENGTH = 5


@dataclass(frozen=True)
class Rectangle:
    width: float
    height: float
    x: float
    y: float

    @property
    def xy(self):
        """
        Returns the coordinates of the rectangle as a tuple (x, y).
        """
        return (int(self.x + 0.5), int(self.y + 0.5))

    @property
    def wh(self):
        """
        Returns the width and height of the rectangle as a tuple (width, height).
        """
        return (math.ceil(self.width), math.ceil(self.height))

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def xyrb(self):
        """
        Returns the coordinates of the rectangle as a tuple (x, y, right, bottom).
        """
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    @property
    def area(self):
        """
        Returns the area of the rectangle.
        """
        return self.width * self.height

    @property
    def rotated_ccw(self):
        """
        Returns a new rectangle that is rotated 90 degrees counter-clockwise.
        """
        return Rectangle(
            x=self.x,
            y=self.y + self.height - self.width,
            width=self.height,
            height=self.width,
        )

    def is_inside(self, other: "Rectangle") -> bool:
        """
        Returns True if the rectangle is inside the other rectangle.

        Args:
            other (Rectangle): The other rectangle.

        Returns:
            bool: True if the rectangle is inside the other rectangle.
        """
        return (
            self.x >= other.x
            and self.y >= other.y
            and self.right <= other.right
            and self.bottom <= other.bottom
        )

    def overlaps(self, other: "Rectangle") -> bool:
        """
        Returns True if the rectangle overlaps with the other rectangle.

        Args:
            other (Rectangle): The other rectangle.

        Returns:
            bool: True if the rectangle overlaps with the other rectangle.
        """
        return (
            self.x < other.right
            and self.right > other.x
            and self.y < other.bottom
            and self.bottom > other.y
        )

    def contains_other(self, other: "Rectangle") -> bool:
        """
        Returns True if the rectangle contains the other rectangle.

        Args:
            other (Rectangle): The other rectangle.

        Returns:
            bool: True if the rectangle contains the other rectangle.
        """
        return other.is_inside(self)

    def __repr__(self):
        return f"Rectangle(x={int(self.x)} y={int(self.y)} w={int(self.width)} h={int(self.height)})"


def _remove_small_rectangles(rectangles: list[Rectangle]) -> list[Rectangle]:
    """
    Removes rectangles that are smaller than the minimum rectangle side length.

    Args:
        rectangles (list[Rectangle]): List of rectangles.

    Returns:
        list[Rectangle]: List of rectangles with the small rectangles removed.
    """
    return [
        rectangle
        for rectangle in rectangles
        if rectangle.height >= MIN_RECTANGLE_SIDE_LENGTH
        and rectangle.width >= MIN_RECTANGLE_SIDE_LENGTH
    ]


def fill_remaining_space_horizontal(
    outer_rect: Rectangle, inner_rect: Rectangle
) -> list[Rectangle]:
    """
    Returns a list of rectangles that fill the remaining space between the outer and inner rectangles.

    Args:
        outer_rect (Rectangle): Outer rectangle.
        inner_rect (Rectangle): Inner rectangle.

    Returns:
        list[Rectangle]: List of rectangles that fill the remaining space.
    """
    # Calculate the remaining space
    remaining_width = outer_rect.width - inner_rect.width
    remaining_height = outer_rect.height - inner_rect.height

    # Calculate the x and y offsets for the inner rectangle
    inner_x_offset = inner_rect.x - outer_rect.x
    inner_y_offset = inner_rect.y - outer_rect.y

    # Create a list to store the rectangles that fill the remaining space
    rectangles = []

    # Top rectangle
    if inner_y_offset > 0:
        rectangles.append(
            Rectangle(
                x=outer_rect.x,
                y=outer_rect.y,
                width=outer_rect.width,
                height=inner_y_offset,
            )
        )

    # Bottom rectangle
    if remaining_height > 0:
        rectangles.append(
            Rectangle(
                x=outer_rect.x,
                y=inner_rect.bottom,
                width=outer_rect.width,
                height=outer_rect.height - inner_y_offset - inner_rect.height,
            )
        )

    # Left rectangle
    if inner_x_offset > 0:
        rectangles.append(
            Rectangle(
                x=outer_rect.x,
                y=inner_rect.y,
                width=inner_x_offset,
                height=inner_rect.height,
            )
        )

    # Right rectangle
    if remaining_width > 0:
        rectangles.append(
            Rectangle(
                x=inner_rect.right,
                y=inner_rect.y,
                width=outer_rect.width - inner_x_offset - inner_rect.width,
                height=inner_rect.height,
            )
        )

    rectangles = _remove_small_rectangles(rectangles)

    return rectangles


def fill_remaining_space_vertical(
    outer_rect: Rectangle, inner_rect: Rectangle
) -> list[Rectangle]:
    """
    Returns a list of rectangles that fill the remaining space between the outer and inner rectangles.

    Args:
        outer_rect (Rectangle): Outer rectangle.
        inner_rect (Rectangle): Inner rectangle.

    Returns:
        list[Rectangle]: List of rectangles that fill the remaining space.
    """
    # Calculate the remaining space
    remaining_width = outer_rect.width - inner_rect.width
    remaining_height = outer_rect.height - inner_rect.height

    # Calculate the x and y offsets for the inner rectangle
    inner_x_offset = inner_rect.x - outer_rect.x
    inner_y_offset = inner_rect.y - outer_rect.y

    # Create a list to store the rectangles that fill the remaining space
    rectangles = []

    # Top rectangle
    if inner_y_offset > 0:
        rectangles.append(
            Rectangle(
                x=inner_rect.x,
                y=outer_rect.y,
                width=inner_rect.width,
                height=inner_y_offset,
            )
        )

    # Bottom rectangle
    if remaining_height > 0:
        rectangles.append(
            Rectangle(
                x=inner_rect.x,
                y=inner_rect.bottom,
                width=inner_rect.width,
                height=outer_rect.height - inner_y_offset - inner_rect.height,
            )
        )

    # Left rectangle
    if inner_x_offset > 0:
        rectangles.append(
            Rectangle(
                x=outer_rect.x,
                y=outer_rect.y,
                width=inner_x_offset,
                height=outer_rect.height,
            )
        )

    # Right rectangle
    if remaining_width > 0:
        rectangles.append(
            Rectangle(
                x=inner_rect.right,
                y=outer_rect.y,
                width=outer_rect.width - inner_x_offset - inner_rect.width,
                height=outer_rect.height,
            )
        )

    rectangles = _remove_small_rectangles(rectangles)

    return rectangles


def _find_gaps_for_img_row(
    img_row: list[int], base_value: int, image_width: int
) -> tuple[list[int], list[int]]:
    """
    Finds the gaps in a row of an image.

    Args:
        img_row (list[int]): The row of the image.
        base_value (int): The base value to compare against (the image background).
        image_width (int): The width of the image.

    Returns:
        tuple[list[int], list[int]]: Tuple containing two lists. The first list contains the indices of the left edges of the gaps, and the second list contains the indices of the right edges of the gaps.
    """
    left_inds = []
    right_inds = []

    # find the gaps between the letters
    left_inds = []
    right_inds = []
    new_rect_active = False
    for col_ind, val in enumerate(img_row):
        if val == base_value and not new_rect_active:
            new_rect_active = True
            left_inds.append(col_ind)
        elif new_rect_active and val != base_value:
            new_rect_active = False
            right_inds.append(col_ind)
        else:
            continue

    if new_rect_active:
        right_inds.append(image_width)

    return left_inds, right_inds


def _make_new_rectangles(
    rectangles: list[Rectangle],
    row_ind: int,
    left_inds: list[int],
    right_inds: list[int],
):

    new_rectangles = []
    for left_ind, right_ind in zip(left_inds, right_inds, strict=True):
        # if the rectangle is too small
        if right_ind - left_ind < MIN_RECTANGLE_SIDE_LENGTH:
            continue
        # if this is a continuation of an existing rectangle
        extended = False
        for rect_ind, rectangle in enumerate(rectangles):
            if (
                rectangle.bottom == row_ind
                and rectangle.x == left_ind
                and rectangle.right == right_ind
            ):
                rectangles[rect_ind] = Rectangle(
                    x=rectangle.x,
                    y=rectangle.y,
                    width=rectangle.width,
                    height=rectangle.height + 1,
                )
                extended = True
                break
        # otherwise it's a new rectangle
        if not extended:
            new_rectangles.append(
                Rectangle(x=left_ind, y=row_ind, width=right_ind - left_ind, height=1)
            )

    return new_rectangles


def fill_space_around_word(
    image: ImageWrapper,
    text_rect: Rectangle,
    fill_direction: str,
) -> list[Rectangle]:
    """
    Returns a list of rectangles that fill the remaining space

    Args:
        image (Image): the overall wordcloud image.
        text_rect (Rectangle): The rectangle containing the new text.
        fill_direction (str): The direction to fill the space in. Either "horizontal" or "vertical".

    Returns:
        list[Rectangle]: List of rectangles that fill the remaining space.
    """

    img = image.img
    background_color = image.background_color

    img_section = img.crop(text_rect.xyrb)
    img_width, img_height = img_section.size

    # get the image data as a 2D array
    img_data = img_section.quantize(2).getdata()

    # find the base value
    base_value = None
    for original, quantised in zip(img_section.getdata(), img_data):
        if original == background_color:
            base_value = quantised
            break

    if base_value is None:
        raise ValueError("The background color was not found in the image.")

    # img_data = [val for val in img_data]
    img_data = list(img_data)
    img_data = [
        img_data[i * img_width : (i + 1) * img_width] for i in range(img_height)
    ]

    # transpose
    if fill_direction == "horizontal":
        img_data = list(zip(*img_data))

    rectangles = [Rectangle(x=0, y=0, width=len(img_data[0]), height=0)]
    for row_ind, img_row in enumerate(img_data):

        if fill_direction == "horizontal":
            img_row = img_row[::-1]

        left_inds, right_inds = _find_gaps_for_img_row(
            img_row, base_value, len(img_data[0])
        )

        new_rectangles = _make_new_rectangles(
            rectangles, row_ind, left_inds, right_inds
        )
        rectangles.extend(new_rectangles)

    rectangles = _remove_small_rectangles(rectangles)

    # if we rotated the image, we need to rotate the rectangles back
    if fill_direction == "horizontal":
        rotated_rectangles = []
        for rectangle in rectangles:
            rotated_rectangles.append(
                Rectangle(
                    x=rectangle.y,
                    y=len(img_data[0]) - (rectangle.x + rectangle.width),
                    width=rectangle.height,
                    height=rectangle.width,
                )
            )
        rectangles = rotated_rectangles

    # offset the rectangles to the correct position
    rectangles = [
        Rectangle(
            x=rectangle.x + text_rect.x,
            y=rectangle.y + text_rect.y,
            width=rectangle.width,
            height=rectangle.height,
        )
        for rectangle in rectangles
    ]

    return rectangles
