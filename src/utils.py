def draw_rectangle(canvas, rectangle):
    canvas.rectangle(
        (
            rectangle.x,
            rectangle.y,
            rectangle.x + rectangle.width,
            rectangle.y + rectangle.height,
        )
    )
