from pathlib import Path

from collections import Counter
from wrdcld import make_word_cloud

with open(Path("examples/dancingmen.txt"), encoding="utf-8") as f:
    contents = f.read()

words = [word.strip(" \n,.!?:-&\"'") for word in contents.split(" ")]
words = [word for word in words if word]
data = Counter(words)

make_word_cloud(data).show()
