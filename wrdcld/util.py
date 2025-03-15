from __future__ import annotations

import os
import sys
from pathlib import Path
from random import Random

if sys.version_info >= (3, 10):
    from typing import TypeAlias

    Color: TypeAlias = tuple[int, int, int]
else:
    from typing import Tuple

    Color = Tuple[int, int, int]


def get_repo_root() -> Path:
    return Path(__file__).parent.parent


_RANDOM_STATE = None


def get_random_state(reseed: bool = False, seed: int | None = None) -> Random:
    """
    Get the current state of the random number generator, or reseed it
    """

    global _RANDOM_STATE  # pylint: disable=global-statement

    if reseed or _RANDOM_STATE is None:
        if seed is not None:
            _RANDOM_STATE = Random(seed)
        else:
            _RANDOM_STATE = Random(int.from_bytes(os.urandom(8), byteorder="big"))

    return _RANDOM_STATE
