import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    res: dict[str, list[str]] = {}
    for k, v in dct.items():
        if v in res:
            res[v].append(k)
        else:
            res[v] = [k]

    return res
