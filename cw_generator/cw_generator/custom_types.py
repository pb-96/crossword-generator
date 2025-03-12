from typing import TypedDict
from enum import Enum

class Config(TypedDict):
    ...


class ReplaceStrategy(Enum):
    # Replace from smallest and find words with fit in given space
    sort_lr: str = "sort_lr"
    # Replace from smallest and find words with fit in given space
    sort_rl: str = "sort_rl"


class CanFit(TypedDict):
    # True if there is not enough space for the chars to fit on the grid
    no_fit: bool
    # Diff in chars
    diff: int
    # cut_off_index
    cut_off_index: int
