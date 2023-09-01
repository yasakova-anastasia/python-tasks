import numpy as np
import numpy.typing as npt


def replace_nans(matrix: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    mean = np.nanmean(matrix)
    inds = np.where(np.isnan(matrix))
    matrix[inds] = mean
    if np.isnan(mean):
        matrix[inds] = 0.0
    return matrix
