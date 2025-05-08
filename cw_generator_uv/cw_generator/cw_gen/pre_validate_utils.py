from typing import List, Tuple
from cw_generator.custom_types import CanFit, ReplaceStrategy


def check_can_fit(dim: int, words: List[str]) -> CanFit:
    # this would reflect all the possible places
    # where the chars in each word could it
    total_space: int = dim * dim
    total_chars = sum((len(word) for word in words))

    no_fit = total_space < total_chars
    diff = (max(total_space, total_chars) - min(total_space, total_chars),)
    cutoff_index = -1

    if no_fit:
        count = 0
        for index, word in enumerate(words):
            if count + len(word) > total_space:
                break
            count += len(word)
        cutoff_index = index

    return_dict: CanFit = {
        "no_fit": no_fit,
        "diff": diff,
        "cut_off_index": cutoff_index,
    }

    return return_dict


def chop_ordered_words(words: List[str], diff_dict: CanFit) -> Tuple[List, List]:
    cut_off = diff_dict["cut_off_index"]
    return words[:cut_off], words[cut_off + 1 :]


def fit_words(words: List[str], replace_strategy: str) -> Tuple[List[str], List[str]]:
    words.sort(key=len, reverse=replace_strategy == ReplaceStrategy.sort_rl.value)
    diff_dict = check_can_fit(len(words), words)
    fitted_words = chop_ordered_words(words, diff_dict)
    return fitted_words
