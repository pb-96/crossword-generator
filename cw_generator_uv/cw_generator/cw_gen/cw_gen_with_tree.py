from typing import List, Tuple,  Dict, Union, Optional, DefaultDict
from collections import defaultdict
from cw_generator.cw_gen.cw_base_class import GeneratorBase, ALL_DIRECTIONS


class Node:
    """Node class representing a letter position in the crossword tree.
    
    Attributes:
        value: The letter value at this position
        pos: The (row, col) position in the grid
        consumed: Whether this position has been used in a word
    """
    __slots__ = ("value", "pos", "consumed")

    def __init__(self, value: str, pos: Tuple[int, int]) -> None:
        """Initialize a new Node.
        
        Args:
            value: The letter value
            pos: The (row, col) position in the grid
        """
        self.value = value
        self.pos = pos
        self.consumed = False

    def __repr__(self) -> str:
        return f"{self.value}:{self.pos}"


class CWTreeGenerator(GeneratorBase):
    """Crossword generator using a tree-based approach for word placement.
    
    This implementation uses a tree structure to track letter positions,
    allowing for more efficient word placement by leveraging existing letters.
    """
    
    def __init__(self, words: List[str], dimensions: int = 15, retry_un_added: bool = False) -> None:
        """Initialize the tree-based crossword generator.
        
        Args:
            words: List of words to place in the crossword
            dimensions: Size of the crossword grid (default: 15)
            retry_un_added: Whether to retry placing unadded words (default: False)
        """
        self.tree: DefaultDict[str, List[Node]] = defaultdict(list)
        super().__init__(words, dimensions, retry_un_added)

    def compare_to_existing(self, word: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Try to place a word by connecting it to existing letters.
        
        Args:
            word: The word to place
            
        Returns:
            Tuple of (start_position, direction) if placement successful, None otherwise
        """
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
        return None

    def place_tup(self, word: str, tup: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        """Place a word at the specified position and direction.
        
        Args:
            word: The word to place
            tup: Tuple of (start_position, direction)
        """
        initial_placement, direction = tup
        for char in word:
            self.tree[char].append(Node(value=char, pos=initial_placement))
            self.cw_matrix[initial_placement[0]][initial_placement[1]] = char
            initial_placement = (
                initial_placement[0] + direction[0],
                initial_placement[1] + direction[1],
            )
            
        # Store word location information
        self.words_by_locations[word] = {
            "location_tuple_start": tup[0],
            "location_tuple_end": initial_placement,
            "direction": direction
        }

    def build_cw(self) -> None:
        """Build the crossword puzzle using the tree-based approach."""
        if not self.words:
            return
            
        words = iter(self.words)
        word = next(words)
        
        # Place first word randomly
        placement = self.place_randomly(word)
        if placement is None:
            self.un_added_words.append(word)
            return
            
        self.place_tup(word, placement)

        # Place remaining words
        for word in words:
            placement = self.compare_to_existing(word) or self.place_randomly(word)
            if placement is not None:
                self.place_tup(word, placement)
            else:
                self.un_added_words.append(word)
