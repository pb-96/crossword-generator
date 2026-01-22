from typing import TypedDict, List, Dict, Tuple, Any
from enum import Enum
from pydantic import BaseModel
from typing import Literal

MATRIX_TYPE = List[List[Any]]


class SupportedCompression(Enum):
    base64 = "base64"


class WordByLocationDict(TypedDict):
    location_tuple_start: Tuple[int, int]
    location_tuple_end: Tuple[int, int]
    description: str
    word: str


class ReplaceStrategy(Enum):
    # Replace from smallest and find words with fit in given space
    sort_lr = "sort_lr"
    # Replace from smallest and find words with fit in given space
    sort_rl = "sort_rl"


class Config(TypedDict):
    default_chunk: int
    sort_strategy: Literal[ReplaceStrategy.sort_lr]
    look_back_weeks: int
    look_back_days: int


class CanFit(TypedDict):
    # True if there is not enough space for the chars to fit on the grid
    no_fit: bool
    # Diff in chars
    diff: int
    # cut_off_index
    cut_off_index: int


class Point(TypedDict):
    start: Tuple[int, int]
    end: Tuple[int, int]
    direction: Tuple[int, int] | None


class CWPoint(BaseModel):
    words_description: Dict[str, str]
    # The inner dict would be {'start': (0,1 ), 'end': (0, 4), 'direction': (0, 1)}
    words_locations: Dict[str, Point]
    cw_matrix: List[List[str]]
