from typing import List, Tuple, TypedDict
from enum import Enum

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

def check_can_fit(dim: int , words: List[str]) -> CanFit:
    # this would reflect all the possible places
    # where the chars in each word could it 
    total_space: int = dim * dim
    total_chars = sum(
        (len(word) for word in words)
    )

    return_dict: CanFit = {
        "no_fit": total_space < total_chars,
        "diff": max(total_space, total_chars) - min(total_space, total_chars),
        "cut_off_index": -1
    }

    if not return_dict["no_fit"]:
        rolling_len = 0
        for index, word in enumerate(words):
            rolling_len += len(word)
            if rolling_len >= total_space:
                break
        return_dict["cut_off_index"] = max(index - 1, 0)

    return return_dict
    


def chop_ordered_words(words: List[str], diff_dict: CanFit) -> Tuple[List, List]:
    cut_off = diff_dict["cut_off_index"]
    diff = diff_dict["diff"]
    pad_remaining = words[cut_off + 1: ]
    pad_remaining.sort(key=len)
    pad_remaining = [word for word in pad_remaining if word <= diff]



def replace_strategy():
    ...