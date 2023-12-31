import numpy as np
import numpy.typing as npt


def add_zeros(x: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    a = np.dstack((x, np.zeros_like(x)))
    a = a.reshape(a.size)
    return a[:-1]
