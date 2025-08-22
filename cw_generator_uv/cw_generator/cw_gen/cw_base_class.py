from typing import Optional, List, Tuple, Dict, Iterator
from collections import OrderedDict
from random import randint, choice
from functools import lru_cache
import string


ALL_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1)]


class GeneratorBase:
    """Base class for crossword puzzle generators.
    
    This class provides the core functionality for generating crossword puzzles,
    including word placement, matrix management, and random letter padding.
    """
    __slots__ = ["cw_matrix"]  # Final matrix is immutable after initialization
    
    def __init__(
        self, words: List[str], dimensions: int = 15, retry_un_added: bool = False
    ) -> None:
        """Initialize the crossword generator.
        
        Args:
            words: List of words to place in the crossword
            dimensions: Size of the crossword grid (default: 15)
            retry_un_added: Whether to retry placing unadded words (default: False)
            
        Raises:
            ValueError: If dimensions is less than 1 or words list is empty
        """
        if not words:
            raise ValueError("Words list cannot be empty")
        if dimensions < 1:
            raise ValueError("Dimensions must be greater than 0")
        # Truthy check is fine for now
        words = [word for word in words if word]
        # Create temporary working matrix
        temp_matrix = [[] for _ in range(dimensions)]
        self.available_start_points = OrderedDict()
        for row in range(dimensions):
            for col in range(dimensions):
                temp_matrix[row].append("X")
                self.available_start_points[(row, col)] = None
        
        self.cw_matrix = temp_matrix
        self.words = words
        self.directions = ALL_DIRECTIONS
        self.un_added_words: List[str] = []
        self.re_try_un_added = retry_un_added
        self.words_by_locations: Dict[str, Dict[str, Tuple[int, int]]] = {}
        
        # Build the crossword using temporary matrix
        self._build_cw_with_matrix(temp_matrix)
        
        # Set the final immutable matrix
        self.cw_matrix = temp_matrix

    def _build_cw_with_matrix(self, matrix: List[List[str]]) -> None:
        """Build the crossword using the provided matrix.
        
        Args:
            matrix: The temporary matrix to build the crossword in
        """
        self.build_cw()
        self._pad_random_letters(matrix)

    def _pad_random_letters(self, matrix: List[List[str]]) -> None:
        """Fill empty spaces with random letters in the provided matrix.
        
        Args:
            matrix: The matrix to pad with random letters
        """
        random_letters = [
            choice(string.ascii_lowercase)
            for _ in range(len(self.available_start_points))
        ]

        for (row, col), random_letter in zip(
            self.available_start_points, random_letters
        ):
            matrix[row][col] = random_letter

    def can_fit_word(
        self,
        word: str,
        start_pos: Tuple[int, int],
        direction: Tuple[int, int],
        word_index: int,
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Check if a word can fit at the given position and direction.
        
        Args:
            word: The word to check
            start_pos: Starting position (row, col)
            direction: Direction vector (row_step, col_step)
            word_index: Index in the word to start from
            
        Returns:
            Tuple of (start_position, direction) if word can fit, None otherwise
        """
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

    def place_randomly(self, word: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Attempt to place a word randomly in the grid.
        
        Args:
            word: The word to place
            
        Returns:
            Tuple of (start_position, direction) if placement successful, None otherwise
        """
        if not self.available_start_points:
            return None
            
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
                break
            random_start = given_keys[ptr]
        return None

    @lru_cache(maxsize=None)
    def search_chunk(
        self, word: str, direction: Tuple[int, int], pos: Tuple[int, int]
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Search for a valid position to place a chunk of a word.
        
        Args:
            word: The word chunk to place
            direction: Direction vector (row_step, col_step)
            pos: Starting position (row, col)
            
        Returns:
            Tuple of (end_position, direction) if valid, None otherwise
        """
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

    def build_cw(self) -> None:
        """Build the crossword puzzle. Must be implemented by subclasses."""
        raise NotImplementedError("Subclass must implement this method")

    def __iter__(self) -> Iterator[List[str]]:
        """Iterate over the rows of the crossword matrix."""
        for line in self.cw_matrix:
            yield line

    def __del__(self):
        """Clean up the lru_cache when the instance is destroyed."""
        self.search_chunk.cache_clear()
