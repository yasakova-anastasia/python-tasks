def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """

    if type1 in [range, tuple] and type2 in [range, tuple]:
        return tuple

    if type1 == type2:
        return type1

    if type1 == range and type2 in [bool, int, float, complex] or \
            type2 == range and type1 in [bool, int, float, complex]:
        return str

    if type1 == str or type2 == str:
        return str

    if type1 in [list, tuple] and type2 in [bool, int, float, complex] or \
            type2 in [list, tuple] and type1 in [bool, int, float, complex]:
        return str

    if type1 == complex or type2 == complex:
        return complex

    if type1 == float or type2 == float:
        return float

    if type1 == int or type2 == int:
        return int

    if type1 == list or type2 == list:
        return list

    if type1 == range or type2 == range:
        return range

    return str
