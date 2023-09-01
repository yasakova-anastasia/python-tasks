from typing import Generator, Any


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """
    :param matrix: rectangular matrix
    :return: transposed matrix
    """
    return [[matrix[i][j] for i in range(len(matrix))]
            for j in range(len(matrix[0]))]


def uniq(sequence: list[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: arbitrary sequence of comparable elements
    :return: generator of elements of `sequence` in
    the same order without duplicates
    """
    elems = set()
    for val in sequence:
        if val not in elems:
            elems.add(val)
            yield val


def dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    :param *dicts: flat dictionaries to be merged
    :return: merged dictionary
    """
    return {k: v for el in dicts for k, v in el.items()}


def product(lhs: list[int], rhs: list[int]) -> int:
    """
    :param rhs: first factor
    :param lhs: second factor
    :return: scalar product
    """
    return sum([rhs[i] * lhs[i] for i in range(len(lhs))])
