from typing import List, cast
import base64
from ast import literal_eval
from cw_generator.custom_types import MATRIX_TYPE, SupportedCompression


def compress_matrix(cw_matrix: MATRIX_TYPE) -> bytes:
    joined_matrix = "".join((" ".join(l) for l in cw_matrix))
    compressed = base64.b64encode(joined_matrix)
    return compressed


def decompress(
    bytes_matrix: bytes, compression_func: SupportedCompression
) -> List[List[str]]:
    match compression_func.value:
        case "base64":
            raw = literal_eval(base64.b64decode(bytes_matrix))
            if isinstance(raw, list) and len(list) > 0 and isinstance(raw[0], list):
                raw = cast(MATRIX_TYPE, raw)
                return raw
            else:
                raise ValueError("Matrix was malformed")


def compress(matrix: MATRIX_TYPE, compression_func: SupportedCompression) -> bytes:
    # default = [[]]
    match compression_func.value:
        case "base64":
            return compress_matrix(matrix)
    # return default


def calculate_direction(): ...
