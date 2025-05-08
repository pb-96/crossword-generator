from typing import List, Tuple, Set
from cw_generator.custom_types import CanFit, ReplaceStrategy
import re

plurals = re.compile(r"(s|es|ies)$")
LEV_DISTANCE = 4

swops_dict = {
    "s": "",
    "es": "",
    "ies": "y",
}


def custom_lev_distance(word_one: str, word_two: str) -> bool:
    # This will look at the lev distance
    # And if the difference is greater then the threshold
    # Check if it is the last [Threshold: ] this is the difference
    # If yes -> then return True
    ...


def singular_only(words: Set[str]) -> bool:
    # This deals with simple plurals
    # Irregular ones would need to dealt with lev distance
    # For now this is good enough
    plurals_set = set()

    for _, word in enumerate(words):
        found = re.search(plurals, word)
        if found:
            key = found.group()
            singular = word[: found.start()] + swops_dict[key]
            plurals_set.add(singular)
        else:
            # APPLY LEV DISTANCE HERE
            continue
    duplicates = plurals_set.union(words)
    return len(duplicates) > 1


def all_words_are_unique(words: List[str]) -> bool:
    unique = {}
    for word in words:
        if word in unique:
            return False
        else:
            unique[word] = True
    return True


def check_can_fit_estimate(dim: int, words: List[str]) -> CanFit:
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


def fit_words(
    words: List[str], replace_strategy: ReplaceStrategy
) -> Tuple[List[str], List[str]]:
    words.sort(key=len, reverse=replace_strategy == ReplaceStrategy.sort_rl)
    diff_dict = check_can_fit_estimate(len(words), words)
    fitted_words = chop_ordered_words(words, diff_dict)
    return fitted_words
