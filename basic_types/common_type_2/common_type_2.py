import typing as tp


def get_types(data: list[tp.Any]) -> list[tp.Any]:
    result = []
    for i in data:
        result.append(type(i))

    return result


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    types = get_types(data)
    common_type = types[0]
    if list in types or tuple in types:
        common_type = list
    elif bool in types:
        common_type = bool
    elif float in types:
        common_type = float
    elif int in types:
        common_type = int
    else:
        common_type = str

    result: tp.List[tp.Any] = []

    for i in data:
        if common_type == list:
            if type(i) in [str, int, bool]:
                if i == "":
                    result.append([])
                else:
                    result.append([i])
            elif i is None:
                result.append([])
            else:
                result.append(common_type(i))
        elif common_type == str:
            if i is None:
                result.append("")
            else:
                result.append(common_type(i))
        elif common_type == int:
            if i is None or i == "":
                result.append(0)
            else:
                result.append(common_type(i))
        elif common_type == float:
            if i is None or i == "":
                result.append(0.0)
            else:
                result.append(common_type(i))
        elif common_type == bool:
            if i is None or i == "":
                result.append(False)
            else:
                result.append(common_type(i))
        else:
            result.append(common_type(i))

    return result
