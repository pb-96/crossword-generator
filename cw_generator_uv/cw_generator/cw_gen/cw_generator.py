from typing import List, Tuple, Optional, Dict, Any
from collections import OrderedDict, defaultdict
import warnings
from cw_generator.cw_gen.cw_base_class import GeneratorBase


class CrossWordGen(GeneratorBase):
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
        return self.cw_matrix
