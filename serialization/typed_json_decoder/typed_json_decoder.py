import typing as tp
import json

from decimal import Decimal


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    def check(dict: tp.Dict[tp.Any, tp.Any]) -> tp.Any:
        val = dict.pop("__custom_key_type__", None)

        if val:
            if val == "int":
                dict = {int(key): val for key, val in dict.items()}
            elif val == "float":
                dict = {float(key): val for key, val in dict.items()}
            else:
                dict = {Decimal(key): val for key, val in dict.items()}
        return dict

    return json.loads(json_value, object_hook=check)
