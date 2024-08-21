import sys
from pathlib import Path

if sys.version_info >= (3, 10):
    from typing import TypeAlias

    Color: TypeAlias = tuple[int, int, int]
else:
    from typing import Tuple

    Color = Tuple[int, int, int]


def get_repo_root():
    return Path(__file__).parent.parent
