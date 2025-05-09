from cw_generator.cw_gen.cw_gen_with_tree import CWTreeGenerator
from typing import List, Tuple
from pre_validate_utils import (
    singular_only,
    all_words_are_unique,
    check_can_fit_estimate,
    merge_strategy,
)
from cw_generator.custom_types import WordByLocationDict, MATRIX_TYPE
import logging


def generate_cw(to_place: List[str]) -> Tuple[WordByLocationDict, MATRIX_TYPE]:
    unique, unique_set = all_words_are_unique(to_place)
    if not unique:
        raise ValueError("Words to place must be unique")

    changes, singular_only_set = singular_only(unique_set)
    if changes:
        logging.warning("Clashes between singular and non singular words present")

    singular_list = [*singular_only_set]

    can_fit = check_can_fit_estimate(singular_list)
    # Need to do an and check on the config to tell if this is wanted
    if can_fit["no_fit"]:
        singular_list = merge_strategy(can_fit, singular_list)

    cross_word_cls = CWTreeGenerator(singular_list)
    return cross_word_cls.words_by_locations, cross_word_cls.cw_matrix
