from cw_generator.cw_gen.cw_gen_with_tree import CWTreeGenerator

from cw_generator.cw_gen.cw_validator import WordSearch, Point
from typing import List, Dict, Tuple


def generate_cw(to_place: List[str]) -> Dict[str, Tuple]:
    # Call validation here
    # Would to ensure the list of words are unique or things would break
    # Needs to read from config here to determine which CW Generator to actually use
    cross_word_cls = CWTreeGenerator(to_place)
    points = {}
    return points
