import numpy as np
import numpy.typing as npt


def vander(array: npt.NDArray[np.float_ | np.int_]) -> npt.NDArray[np.float_]:
    """
    Create a Vandermod matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    res = np.ones(array.size)[:, np.newaxis]
    while res.shape != (array.size, array.size):
        res = np.hstack((res, array[:, np.newaxis] * res[:, -1][:, np.newaxis]))

    return res
