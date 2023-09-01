def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    return [a ** 2 for a in elements]


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    return [i + 1 for i in range(len(elements))]


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    if not len(elements):
        return None

    max = 0
    idx = 0
    for i, val in enumerate(elements):
        if val > max:
            max = val
            idx = i

    return idx


# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    if len(elements) < 2:
        return []
    return [elements[i * 2 + 1] for i in range(len(elements) // 2)]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    for i, val in enumerate(elements):
        if val == 3:
            return i
    return None


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    for i in range(len(elements) - 1, -1, -1):
        if elements[i] == 3:
            return i
    return None


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: int | None) -> tuple[int | None, int | None]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    if not len(elements):
        return (default, default)

    return (min(elements), max(elements))


# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> int | None:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return val if (val := elements[i]) > boundary else None
