# wrdcld
A predictable, interpretable wordcloud library

`wrdcld` is available to install via pip

```bash
pip install wrdcld
```

## Basic Usage

To make a basic wordcloud, you simply pass a list of words to the `make_wordcloud` function. Here is a basic example generating a word cloud of the Sherlock Holmes story __The adventure of the dancing men__.

```python
from pathlib import Path

from wrdcld import make_word_cloud

contents = Path("examples/dancingmen.txt").read_text()

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
Run `poetry install`

## Development
Run `poetry run isort wrdcld tests`, `poetry run black wrdcld tests` and `poetry run pylint wrdcld tests` for styling and linting.

## Testing
Run `python -m unittest discover tests/`
