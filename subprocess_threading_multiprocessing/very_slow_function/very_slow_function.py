import time
from threading import Thread
import multiprocessing


def very_slow_function(x: int) -> int:
    """Function which calculates square of given number really slowly
    :param x: given number
    :return: number ** 2
    """
    time.sleep(0.3)
    return x ** 2


def calc_squares_simple(bound: int) -> list[int]:
    """Function that calculates squares of numbers in range [0; bound)
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    res = []
    for i in range(bound):
        res.append(very_slow_function(i))
    return res


def calc_squares_multithreading(bound: int) -> list[int]:
    """Function that calculates squares of numbers in range [0; bound)
    using threading.Thread
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    def func(results: list[int], i: int) -> None:
        results[i] = very_slow_function(i)

    res = [0] * bound
    threads = []
    for i in range(bound):
        threads.append(Thread(target=func, args=(res, i)))
        threads[-1].start()

    for thread in threads:
        thread.join()

    return res


def calc_squares_multiprocessing(bound: int) -> list[int]:
    """Function that calculates squares of numbers in range [0; bound)
    using multiprocessing.Pool
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    with multiprocessing.Pool() as pool:
        result = pool.map(very_slow_function, range(bound))
    return result
