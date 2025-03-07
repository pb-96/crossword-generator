from typing import List, Tuple, Optional, Dict, Any
from collections import OrderedDict, defaultdict
from random import randint, choice
from functools import lru_cache
import string
import warnings

ALL_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]


class CrossWordGen:
    slots = ["cw_matrix"]

    def __init__(
        self, words: List[str], dimensions: int = 15, retry_un_added: bool = False
    ):
        self.cw_matrix = [[] for _ in range(dimensions)]
        self.available_start_points = OrderedDict()
        for row in range(dimensions):
            for col in range(dimensions):
                self.cw_matrix[row].append("X")
                self.available_start_points[(row, col)] = None

        self.words = sorted(words, key=len, reverse=True)
        directions = ALL_DIRECTIONS
        self.directions = directions
        # Exclude these a from testing suite
        self.un_added_words = []
        self.re_try_un_added = retry_un_added
        self.build_cw()

    def place_randomly(self, word: str) -> Optional[Tuple]:
        random_index = randint(0, len(self.available_start_points))
        given_keys = list(self.available_start_points.keys())
        random_start = given_keys[random_index]
        ptr = int(random_index)

        while ptr != (random_index - 1):
            for direction in self.directions:
                starting_point = self.search_chunk(word, direction, random_start)
                if starting_point:
                    return random_start, direction
            ptr = (ptr + 1) % len(self.available_start_points)
            random_start = given_keys[ptr]
        return None

    @lru_cache(maxsize=None)
    def search_chunk(self, word: str, direction: Tuple[int, int], pos: Tuple[int, int]):
        r, c = pos
        for _ in range(len(word)):
            r, c = r + direction[0], c + direction[1]
            if not (
                r >= 0
                and r < len(self.cw_matrix)
                and c >= 0
                and c < len(self.cw_matrix[0])
            ):
                return None

            if self.cw_matrix[r][c] != "X":
                return None

        return (r, c), direction

    def can_fit_word(
        self,
        word: str,
        start_pos: Tuple[int, int],
        direction: Tuple[int, int],
        word_index: int,
    ) -> Optional[Tuple[int, int]]:

        row_step, col_step = direction
        word_len = len(word) - 1
        left, right = word[:word_index], word[word_index:word_len]
        opposite_direction = (-row_step, -col_step)

        R = self.search_chunk(right, direction, tuple(start_pos))
        if R is None:
            return None

        _, direction = R
        L = self.search_chunk(left, opposite_direction, tuple(start_pos))

        if L is None:
            return None

        start, _ = L
        return start, R[1]

    def compare_to_last_added(self, last_added: Dict[str, Any], word):
        last_added_key = list(last_added.keys())[-1]
        last_added_word = last_added[last_added_key]

        for index, char in enumerate(word):
            starting_positions = last_added_word.get(char) or []
            for start_pos in starting_positions:
                for direction in self.directions:
                    start_point = self.can_fit_word(word, start_pos, direction, index)
                    if start_point is None:
                        continue
                    return start_point

    def check_valid_placement(
        self, word: str, last_added: OrderedDict[str, Dict]
    ) -> Optional[Tuple]:
        if not last_added:
            return self.place_randomly(word)

        joint = self.compare_to_last_added(last_added, word)
        if joint is not None:
            return joint

        if not self.available_start_points:
            return None

        return self.place_randomly(word)

    def build_cw(self):
        lst_added = OrderedDict()
        for word in self.words:
            T = self.check_valid_placement(word, lst_added)
            if T is None:
                # This is where invalid words would be registered
                self.un_added_words(word)
                warnings.warn(f"could not add word to matrix: {word}")
                continue

            initial_placement, given_direction = T
            rolling_indexes = []
            for char in word:
                row, col = initial_placement
                rolling_indexes.append((row, col))
                self.available_start_points.pop((row, col), None)
                self.cw_matrix[row][col] = char
                initial_placement = (
                    row + given_direction[0],
                    col + given_direction[1],
                )

            this_word = defaultdict(list)
            for word, indexes in zip(word, rolling_indexes):
                this_word[word].append(indexes)
            lst_added[word] = this_word

        random_letters = [
            choice(string.ascii_lowercase)
            for _ in range(len(self.available_start_points))
        ]

        for (row, col), random_letter in zip(
            self.available_start_points, random_letters
        ):
            self.cw_matrix[row][col] = random_letter

        return self.cw_matrix

    def __iter__(self):
        for line in self.cw_matrix:
            yield line
