from typing import List, Tuple, TypedDict
from enum import Enum
from collections import deque, defaultdict


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


def check_can_fit(dim: int, words: List[str]) -> CanFit:
    # this would reflect all the possible places
    # where the chars in each word could it
    total_space: int = dim * dim
    total_chars = sum((len(word) for word in words))

    no_fit = total_space < total_chars
    diff = max(total_space, total_chars) - min(total_space, total_chars),
    cutoff_index = -1

    if no_fit:
        # Maybe best to pre sort so it can be easily adjusted by the config management
        words.sort(key=len)
        count = 0
        for index, word in enumerate(words):
            if count + len(word) > total_space:
                break
            count += len(word)
        cutoff_index = index

    return_dict: CanFit = {
        "no_fit": no_fit,
        "diff": diff,
        "cut_off_index": cutoff_index
    }

    return return_dict


def chop_ordered_words(words: List[str], diff_dict: CanFit) -> Tuple[List, List]:
    cut_off = diff_dict["cut_off_index"]
    return words[: cut_off], words[cut_off + 1: ]


def replace_strategy(): ...
