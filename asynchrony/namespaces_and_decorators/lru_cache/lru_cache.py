from collections import OrderedDict
from collections.abc import Callable
from typing import Any, TypeVar, cast

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """
    def func(user_func: Function) -> Function:
        cache: OrderedDict[Any, Any] = OrderedDict()
        full_cache = False

        def wrapper(*args, **kwargs):  # type: ignore
            nonlocal full_cache

            keys = args
            if kwargs:
                for item in kwargs.items():
                    keys += item

            val = cache.get(keys)
            if val is not None:
                return val

            res = user_func(*args, **kwargs)
            if full_cache:
                cache.popitem(last=False)
                cache[keys] = res
            else:
                cache[keys] = res
                full_cache = (len(cache) >= max_size)

            return res

        wrapper.__name__ = user_func.__name__
        wrapper.__doc__ = user_func.__doc__
        wrapper.__module__ = user_func.__module__

        return cast(Function, wrapper)

    return func
