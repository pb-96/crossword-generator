from typing import List
import unittest

from cw_generator.cw_gen.cw_validator import WordSearch
from cw_generator.cw_gen.cw_gen_with_tree import CWTreeGenerator

def alter_input(cw: CWTreeGenerator, in_place: List[str]) -> None:
    if cw.re_try_un_added and cw.un_added_words:
        in_place = [*set(cw.un_added_words).difference(set(in_place))]


class GeneratorTest(unittest.TestCase):
    def test_base_case(self):
        to_place = [
            "clojure",
            "elixir",
            "ecmascript",
            "lansdownerfc",
            "rust",
            "java",
            "lua",
            "lisp",
            "ruby",
        ]

        cw: CWTreeGenerator = CWTreeGenerator(words=to_place)
        validator = WordSearch(puzzle=cw.cw_matrix)
        all_found = all((validator.search(word) for word in to_place))
        assert all_found

    def test_on_to_retry(self): ...
