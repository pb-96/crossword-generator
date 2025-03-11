from typing import List, Tuple, Dict
from collections import defaultdict, OrderedDict
from .cw_generator import CrossWordGen

ALL_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]


class Node:
    def __init__(self, value: str, pos: Tuple[int, int]):
        self.value = value
        self.pos = pos


class CWTrieGenerator(CrossWordGen):
    def __init__(self, words, dimensions=15, retry_un_added=False):
        self.tree: Dict[str, List[Node]] = {}
        super().__init__(words, dimensions, retry_un_added)

    def place(self, word_placements: Dict[str, int]): ...

    def build_cw(self):
        for word in self.words:
            if not self.tree:
                self.place_randomly(word)
            