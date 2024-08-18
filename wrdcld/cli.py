import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a word cloud.")

    parser.add_argument(
        "words",
        type=str,
        help="Path to a file containing words to include in the word cloud.",
    )

    parser.add_argument(
        "--width", type=int, default=500, help="Width of the word cloud image."
    )

    parser.add_argument(
        "--height", type=int, default=500, help="Height of the word cloud image."
    )

    parser.add_argument(
        "--font-color",
        type=int,
        nargs=3,
        default=(255, 255, 0),
        metavar=("R", "G", "B"),
        help="Font color of the words in RGB format.",
    )

    parser.add_argument(
        "--background-color",
        type=int,
        nargs=3,
        default=(73, 109, 137),
        metavar=("R", "G", "B"),
        help="Background color of the word cloud in RGB format.",
    )

    parser.add_argument(
        "--min-font-size", type=int, default=1, help="Minimum font size for the words."
    )

    parser.add_argument(
        "--max-font-size",
        type=int,
        default=100,
        help="Maximum font size for the words.",
    )

    parser.add_argument(
        "--word-padding", type=int, default=0, help="Padding between words."
    )

    parser.add_argument(
        "--show", action="store_true", help="Show the generated word cloud image."
    )

    parser.add_argument(
        "--output-path", type=str, help="Path to save the generated word cloud image."
    )

    return parser.parse_args()
