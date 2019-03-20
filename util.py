import math
from typing import Tuple


def canonize_number(value: int) -> Tuple[float, str]:
    if value == 0:
        return 0, ""
    suffix = ("", "k", "m", "g", "t", "p", "e", "z", "y")
    i = int(math.floor(math.log(value, 1000)))
    p = math.pow(1000, i)
    s = round(value / p, 3)
    return s, suffix[i]


def canonize_size(size_bytes: int) -> Tuple[float, str]:
    if size_bytes == 0:
        return 0, "b"
    size_name = ("b", "kb", "mb", "gb", "tb", "pb", "eb", "zb", "yb")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return s, size_name[i]
