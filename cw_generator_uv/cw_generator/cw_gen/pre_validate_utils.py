from typing import List, Tuple, Set, cast
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


def singular_only(words: Set[str]) -> Tuple[bool, Set[str]]:
    # This deals with simple plurals
    # Irregular ones would need to dealt with lev distance
    # For now this is good enough
    plurals_set = set()
    to_remove = set()

    for _, word in enumerate(words):
        found = re.search(plurals, word)
        if found:
            key = found.group()
            to_remove.add(key)
            singular = word[: found.start()] + swops_dict[key]
            plurals_set.add(singular)
        else:
            # APPLY LEV DISTANCE HERE
            continue

    duplicates = plurals_set.union(words)
    singular_only = to_remove.difference(words)
    return len(duplicates) > 1, singular_only


def all_words_are_unique(words: List[str]) -> Tuple[bool, Set[str]]:
    unique = {}
    for word in words:
        if word in unique:
            return False, set()
        else:
            unique[word] = True
    return True, set(*unique.keys())


def check_can_fit_estimate(dim: int, words: List[str]) -> CanFit:
    # Would need to add the general config file here
    words.sort()
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


def merge_strategy(can_fit: CanFit, words: List[str]) -> List[str]:
    rem = words[can_fit["cut_off_index"] :]
    rolling_diff = can_fit["diff"]
    extra_words = []

    for word in rem:
        word_len = len(word)
        if word_len < rolling_diff:
            extra_words.append(word)
            rolling_diff = rolling_diff - word_len

        if rolling_diff < 0:
            break

    chosen = cast(list, word[can_fit["cut_off_index"] :])
    chosen.extend(extra_words)
    return chosen
