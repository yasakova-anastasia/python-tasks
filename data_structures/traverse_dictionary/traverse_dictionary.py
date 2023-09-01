import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result: list[tuple[str, int]] = []

    def rec_func(dict: tp.Mapping[str, tp.Any], keys: str = "") -> None:
        for k, v in dict.items():
            if type(v) == int:
                result.append((keys + k, v))
            else:
                rec_func(v, keys + k + ".")

    rec_func(dct, prefix)

    return result


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    def rec_func(dict: tp.Mapping[str, tp.Any], keys: str = "") -> None:
        for k, v in dict.items():
            if type(v) == int:
                result.append((keys + k, v))
            else:
                rec_func(v, keys + k + ".")

    rec_func(dct, prefix)


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
        ) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result: list[tuple[str, int]] = []
    stack = [("", dct)]

    while len(stack):
        curr = stack[-1]
        stack.pop()
        for k, v in curr[1].items():
            if type(v) == int:
                result.append((curr[0] + k, v))
            else:
                stack.append((curr[0] + k + ".", v))

    return result
