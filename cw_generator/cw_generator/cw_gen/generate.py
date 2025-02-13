from cw_generator.cw_generator.cw_gen.cw_generator import CrossWordGen
from cw_generator.cw_generator.cw_gen.cw_validator import WordSearch, Point
from typing import List, Dict, Tuple, cast


def generate_cw(to_place: List[str]) -> Dict[str, Tuple]:
    cross_word_cls = CrossWordGen(to_place)
    searcher = WordSearch(puzzle=cross_word_cls.cw_matrix)

    points = {}
    for word in to_place:
        point = searcher.search(word)
        if point is None:
            continue
        point = cast(Point, point)
        points[word] = (point.x, point.y)

    return points
