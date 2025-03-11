from typing import List
import base64

def compress_matrix(cw_matrix: List[List[str]]) -> bytes:
    joined_matrix = "".join(
        (" ".join(l) for l in cw_matrix)
    )
    compressed = base64.b64encode(joined_matrix)
    return compressed
