from .cli import parse_args
from .main import make_word_cloud


def load_words_from_file(file_path):
    try:
        with open(file_path, encoding="utf-8") as file:
            contents = file.read()

        all_words = [word.strip(" \n,.!?:-&\"'[]") for word in contents.split(" ")]
        all_words = [word for word in all_words if word]
        return all_words

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied for file {file_path}.")
    except IsADirectoryError:
        print(f"Error: {file_path} is a directory, not a file.")

    return []


def main():
    args = parse_args()

    all_words = load_words_from_file(args.words)

    word_cloud_image = make_word_cloud(
        all_words=all_words,
        width=args.width,
        height=args.height,
        font_color=tuple(args.font_color),
        background_color=tuple(args.background_color),
        minimum_font_size=args.min_font_size,
        maximum_font_size=args.max_font_size,
        word_padding=args.word_padding,
    )

    if args.output_path:
        word_cloud_image.save(args.output_path)
        print(f"Word cloud saved to {args.output_path}")

    if args.show:
        word_cloud_image.show()


if __name__ == "__main__":
    main()
