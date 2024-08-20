from pathlib import Path
from typing import TypeAlias

Color: TypeAlias = tuple[int, int, int]


def get_repo_root():
    return Path(__file__).parent.parent
