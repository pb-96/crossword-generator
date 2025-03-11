from typing import List, cast, Any
import base64
from ast import literal_eval

MATRIX_TYPE = List[List[Any]]


def compress_matrix(cw_matrix: List[List[str]]) -> bytes:
    joined_matrix = "".join((" ".join(l) for l in cw_matrix))
    compressed = base64.b64encode(joined_matrix)
    return compressed


def decompress(bytes_matrix: bytes, compression_func: str) -> List[List[str]]:
    default = [[]]
    match compression_func:
        case "base64":
            raw = literal_eval(base64.b64decode(bytes_matrix))
            if isinstance(raw, list) and len(list) > 0 and isinstance(raw[0], list):
                raw = cast(MATRIX_TYPE, raw)
                return raw

    return default
