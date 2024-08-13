from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class Rectangle:
    width: float
    height: float
    x: float
    y: float

    @property
    def xy(self):
        return (int(self.x + 0.5), int(self.y + 0.5))

    @property
    def wh(self):
        return (math.ceil(self.width), math.ceil(self.height))

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def xyrb(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    @property
    def area(self):
        return self.width * self.height

    @property
    def rotated_ccw(self):
        return Rectangle(
            x=self.x,
            y=self.y + self.height - self.width,
            width=self.height,
            height=self.width,
        )

    def __repr__(self):
        return f"Rectangle(x={int(self.x)} y={int(self.y)} w={int(self.width)} h={int(self.height)})"


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

    return rectangles

def fill_space_around_word(
    img,
    outer_rect: Rectangle,
    fill_direction: str,
) -> list[Rectangle]:
    """
    Returns a list of rectangles that fill the remaining space

    Args:
        img (Image): the overaall wordcloud image.
        inner_rect (Rectangle): The rectangle containing the new text.

    Returns:
        list[Rectangle]: List of rectangles that fill the remaining space.
    """

    img_section = img.crop(outer_rect.xyrb)
    img_data = np.array(img_section.quantize(2))
    
    if fill_direction == "horizontal":
        img_data = img_data.T


    base_value = img_data[0,0]
    min_rectangle_side_length = 5

    rectangles = [Rectangle(x=0,y=0, width=img_data.shape[1], height=0)]
    for row_ind, img_row in enumerate(img_data):

        if fill_direction == "horizontal":
            img_row = img_row[::-1]

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
            right_inds.append(img_data.shape[1])

        new_rectangles = []
        for left_ind, right_ind in zip(left_inds, right_inds, strict=True):
            # if the rectangle is too small
            if right_ind - left_ind < min_rectangle_side_length:
                continue
            # if this is a continuation of an existing rectangle
            extended = False
            for rect_ind, rectangle in enumerate(rectangles):
                if rectangle.bottom == row_ind and rectangle.x == left_ind and rectangle.right == right_ind:
                    rectangles[rect_ind] = Rectangle(x=rectangle.x, y=rectangle.y, width=rectangle.width, height=rectangle.height+1)
                    extended = True
            # otherwise it's a new rectangle
            if not extended:
                new_rectangles.append(Rectangle(x=left_ind, y=row_ind, width=right_ind-left_ind, height=1))

        rectangles += new_rectangles

    # if we rotated the image, we need to rotate the rectangles back
    if fill_direction == "horizontal":
        rotated_rectangles = []
        for rectangle in rectangles:
            rotated_rectangles.append(Rectangle(
                x=rectangle.y,
                y=img_data.shape[1] - (rectangle.x + rectangle.width) ,
                width=rectangle.height,
                height=rectangle.width
        ))
        rectangles = rotated_rectangles
        
    # offset the rectangles to the correct position
    rectangles = [
        Rectangle(x=rectangle.x + outer_rect.x, y=rectangle.y + outer_rect.y, width=rectangle.width, height=rectangle.height)
        for rectangle in rectangles 
        if rectangle.height >= min_rectangle_side_length and rectangle.width >= min_rectangle_side_length
    ]

    return rectangles