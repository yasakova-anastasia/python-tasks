from typing import Iterable, Generator, Any


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    for val in sequence:
        if val != sequence \
                and hasattr(val, '__iter__'):
            sub_gen = flat_it(val)
            while True:
                try:
                    yield next(sub_gen)
                except StopIteration:
                    break
        else:
            yield val
