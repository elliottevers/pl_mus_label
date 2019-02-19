from typing import List


def intersection(former: List, latter: List) -> List:
    return [value for value in former if value in latter]
