import unittest
from cw_generator.cd_generator import CrossWordGen
from cw_generator.cd_validator import WordSearch


class Generator_test(unittest.TestCase):
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

        cw = CrossWordGen(words=to_place)
        validator = WordSearch(puzzle=cw.cw_matrix)
        all_found = all((validator.search(word) for word in to_place))
        assert all_found