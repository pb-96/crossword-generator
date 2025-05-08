from typing import List, Tuple, Dict, Union
from collections import defaultdict
from cw_generator.cw_gen.cw_base_class import GeneratorBase

ALL_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]


class Node:
    __slots__ = ("value", "pos", "consumed")

    def __init__(self, value: str, pos: Tuple[int, int]):
        self.value = value
        self.pos = pos
        self.consumed = False

    def __repr__(self):
        return f"{self.value}:{self.pos}"


class CWTreeGenerator(GeneratorBase):
    def __init__(self, words, dimensions=15, retry_un_added=False):
        self.tree: Dict[str, List[Node]] = defaultdict(list)
        super().__init__(words, dimensions, retry_un_added)

    def compare_to_existing(self, word: str) -> Union[Tuple, None]:
        for idx, letter in enumerate(word):
            if letter not in self.tree:
                continue
            for node in self.tree[letter]:
                if node.consumed:
                    continue
                for direction in ALL_DIRECTIONS:
                    can_fit = self.can_fit_word(word, node.pos, direction, idx)
                    if can_fit is not None:
                        node.consumed = True
                        return can_fit

    def place_tup(self, word: str, tup: Tuple) -> None:
        initial_placement, direction = tup
        for char in word:
            self.tree[char].append(Node(value=char, pos=initial_placement))
            self.cw_matrix[initial_placement[0]][initial_placement[1]] = char
            initial_placement = (
                initial_placement[0] + direction[0],
                initial_placement[1] + direction[1],
            )
        # Should direction go here though
        self.words_by_locations[word] = {
            "locatoin_tuple_start": tup[0],
            "locatoin_tuple_start": initial_placement,
        }

    def build_cw(self):
        words = iter(self.words)
        word = next(words)
        self.place_tup(word, self.place_randomly(word))

        for word in words:
            T = self.compare_to_existing(word) or self.place_randomly(word)
            if T is not None:
                self.place_tup(word, T)
            else:
                self.un_added_words.append(word)
