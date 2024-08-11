from dataclasses import dataclass


@dataclass
class Rectangle:
    width: float
    height: float
    x: float
    y: float

    @property
    def area(self):
        return self.width * self.height


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
                y=inner_rect.y + inner_rect.height,
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
                x=inner_rect.x + inner_rect.width,
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
                y=inner_rect.y + inner_rect.height,
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
                x=inner_rect.x + inner_rect.width,
                y=outer_rect.y,
                width=outer_rect.width - inner_x_offset - inner_rect.width,
                height=outer_rect.height,
            )
        )

    return rectangles
