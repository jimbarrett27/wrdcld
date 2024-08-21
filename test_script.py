from wrdcld.font import FontWrapper

font = FontWrapper(
    color_func=lambda _: (0, 0, 0), path=FontWrapper.default_font(), size=10000
)
font_size = font.find_fontsize_for_width(10, '0')