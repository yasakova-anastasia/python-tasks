import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return max element before zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """
    matrix = array[1:][(array == 0)[:-1]]
    if matrix.size == 0:
        return None
    return np.max(matrix)
