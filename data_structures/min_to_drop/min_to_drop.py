import typing as tp
from collections import Counter


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    if not seq:
        return 0

    amount = dict(Counter(seq))
    return len(seq) - max(amount.values())
