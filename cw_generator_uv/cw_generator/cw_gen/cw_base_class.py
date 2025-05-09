from typing import Optional, List, Tuple
from collections import OrderedDict
from random import randint, choice
from functools import lru_cache
import string


ALL_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]


class GeneratorBase:
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
        # Surely this where one of the enums about ordering comes into play?
        # Words should be sorted already
        self.words = words
        self.directions = ALL_DIRECTIONS
        # Exclude these a from testing suite
        self.un_added_words = []
        self.re_try_un_added = retry_un_added
        self.words_by_locations = {}
        self.build_cw()
        self.pad_random_letters()

    def can_fit_word(
        self,
        word: str,
        start_pos: Tuple[int, int],
        direction: Tuple[int, int],
        word_index: int,
    ) -> Optional[Tuple[Tuple[int, int]],]:
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

    def place_randomly(self, word: str) -> Optional[Tuple]:
        random_index = randint(0, len(self.available_start_points) - 1)
        given_keys = list(self.available_start_points.keys())
        random_start = given_keys[random_index]
        ptr = int(random_index)

        while ptr != (random_index - 1):
            for direction in self.directions:
                starting_point = self.search_chunk(word, direction, random_start)
                if starting_point:
                    return random_start, direction
            ptr = (ptr + 1) % len(self.available_start_points)
            if ptr == 0:
                # Could not place word
                break
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

    def build_cw(self):
        raise NotImplementedError("Subclass must implement this method")

    def pad_random_letters(self) -> None:
        random_letters = [
            choice(string.ascii_lowercase)
            for _ in range(len(self.available_start_points))
        ]

        for (row, col), random_letter in zip(
            self.available_start_points, random_letters
        ):
            self.cw_matrix[row][col] = random_letter

    def __iter__(self):
        for line in self.cw_matrix:
            yield line
