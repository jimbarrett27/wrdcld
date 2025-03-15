# wrdcld
A predictable, interpretable wordcloud library

`wrdcld` is available to install via pip

```bash
pip install wrdcld
```

## Basic Usage

To make a basic wordcloud, you simply pass a list of words to the `make_word_cloud` function. Here is a basic example generating a word cloud of the Sherlock Holmes story __The adventure of the dancing men__.

```python
from pathlib import Path

from wrdcld import make_word_cloud

contents = Path("examples/dancingmen.txt").read_text(encoding="utf-8")

all_words = [word.strip(" \n,.!?:-&\"'[]") for word in contents.split(" ")]
all_words = [word for word in all_words if word]

make_word_cloud(
    all_words=all_words,
    font_color=(0, 0, 0), # RGB
    background_color=(255, 255, 255),
    minimum_font_size=5,
).show()
```

# Development

## Setup
Run `uv sync`

## Development
Run `uv run isort wrdcld tests examples`, `uv run black wrdcld tests examples`, `uv run pylint wrdcld tests examples` and `uv run mypy wrdcld tests examples` for styling and linting.

## Testing
Run `uv run python -m unittest discover tests/`
